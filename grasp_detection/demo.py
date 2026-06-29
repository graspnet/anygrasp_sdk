import os
import argparse
import numpy as np
import open3d as o3d
from PIL import Image

from gsnet import create_detector
from graspnetAPI import GraspGroup

parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint_path', required=True, help='Model checkpoint path')
parser.add_argument('--max_gripper_width', type=float, default=0.1, help='Maximum gripper width (<=0.1m)')
parser.add_argument('--gripper_height', type=float, default=0.03, help='Gripper height')
parser.add_argument('--vis', action='store_true', help='Enable visualization')
cfgs = parser.parse_args()
cfgs.max_gripper_width = max(0, min(0.1, cfgs.max_gripper_width))

def load_point_cloud(data_dir):
    # get data
    colors = np.array(Image.open(os.path.join(data_dir, 'color.png')), dtype=np.float32) / 255.0
    depths = np.array(Image.open(os.path.join(data_dir, 'depth.png')))
    seg_mask = np.array(Image.open(os.path.join(data_dir, 'seg_mask.png')))

    # get camera intrinsics
    fx, fy = 927.17, 927.37
    cx, cy = 651.32, 349.62
    scale = 1000.0

    # get point cloud
    xmap, ymap = np.arange(depths.shape[1]), np.arange(depths.shape[0])
    xmap, ymap = np.meshgrid(xmap, ymap)
    points_z = depths / scale
    points_x = (xmap - cx) / fx * points_z
    points_y = (ymap - cy) / fy * points_z

    # set your workspace to crop point cloud
    depth_trunc = 1
    mask = (points_z > 0) & (points_z < depth_trunc)
    points = np.stack([points_x, points_y, points_z], axis=-1)
    points = points[mask].astype(np.float32)
    colors = colors[mask].astype(np.float32)
    seg_mask = seg_mask[mask]

    return points, colors, seg_mask

def convert_numpy_to_open3d(points, colors=None):
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        cloud.colors = o3d.utility.Vector3dVector(colors)
    return cloud

def render_results(points, colors, grasp_group, plot_top1=False):
    cloud = convert_numpy_to_open3d(points, colors)
    trans_mat = np.array([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]])
    cloud.transform(trans_mat)
    grippers = grasp_group.to_open3d_geometry_list()
    for gripper in grippers:
        gripper.transform(trans_mat)
    o3d.visualization.draw_geometries([*grippers, cloud])
    if plot_top1:
        o3d.visualization.draw_geometries([grippers[0], cloud])

def predict_with_configs(
        detector,
        points,
        region_steering=None,
        approach_steering=None,
        approach_thresh=np.pi,
        dense_grasp=False,
        collision_detection=True,
    ):
    """AnyGrasp inference."""
    optional_params = {
        "dense_grasp": dense_grasp,
        "collision_detection": collision_detection,
        "region_steering": region_steering,
        "approach_steering": approach_steering,
        "approach_thresh": approach_thresh,
    }
    gg = detector.get_grasp(points, optional_params)
    if gg is None:
        print('No grasp output!')
        return None

    if not dense_grasp:
        gg = gg.nms()
    gg = gg.sort_by_score()
    gg_pick = gg[0:20]
    print("Top 20 scores:")
    print(gg_pick.scores)

    return gg

def demo_default(detector, points, colors, vis=False):
    """Default AnyGrasp with predicted object mask and collision filtering."""
    gg = predict_with_configs(detector, points)

    if gg is not None and vis:
        render_results(points, colors, gg, plot_top1=True)

def demo_region_steering(detector, points, colors, seg_mask, object_id, dense_grasp=False, collision_detection=True, vis=False):
    """Steering AnyGrasp with spcific region mask."""
    gg = predict_with_configs(
        detector,
        points,
        region_steering=(seg_mask==object_id),
        dense_grasp=dense_grasp,
        collision_detection=collision_detection,
    )

    if gg is not None and vis:
        render_results(points, colors, gg)

def demo_approach_steering(detector, points, colors, approach_steering=[0,0,1], approach_thresh=0, vis=False):
    """Steering AnyGrasp with spcific approach vector."""
    gg = predict_with_configs(
        detector,
        points,
        approach_steering=approach_steering,
        approach_thresh=approach_thresh,
    )

    if vis:
        render_results(points, colors, gg)

def demo_workspace_filtering(detector, points, colors, lims, vis=False):
    """Steering AnyGrasp with spcific workspace range."""
    workspace_mask = (points[:,0] >= lims[0]) & (points[:,0] <= lims[1])\
                    & (points[:,1] >= lims[2]) & (points[:,1] <= lims[3])\
                    & (points[:,2] >= lims[4]) & (points[:,2] <= lims[5])

    gg = predict_with_configs(
        detector,
        points,
        region_steering=workspace_mask,
    )

    if gg is not None and vis:
        render_results(points, colors, gg)


def main(data_dir):
    detector = create_detector(cfgs)
    if not detector:
        print("Failed to create detector!")
        return

    points, colors, seg_mask = load_point_cloud(data_dir)

    # Defaul AnyGrasp
    demo_default(detector, points, colors, vis=cfgs.vis)

    # Region steering
    demo_region_steering(detector, points, colors, seg_mask, object_id=1, dense_grasp=False, collision_detection=True, vis=cfgs.vis)
    # Region steering with dense prediction
    demo_region_steering(detector, points, colors, seg_mask, object_id=1, dense_grasp=True, collision_detection=True, vis=cfgs.vis)
    # If you do not care about collision and want more predictions
    demo_region_steering(detector, points, colors, seg_mask, object_id=1, dense_grasp=True, collision_detection=False, vis=cfgs.vis)

    # Approach steering with angle threshold = 60 degrees
    demo_approach_steering(detector, points, colors, approach_steering=[0,5,1], approach_thresh=np.pi/3, vis=cfgs.vis)
    # Approach steering with strict alignment
    demo_approach_steering(detector, points, colors, approach_steering=[0,5,1], approach_thresh=0, vis=cfgs.vis)
    # If you want predictions in top-down views
    demo_approach_steering(detector, points, colors, approach_steering=[0,0,1], approach_thresh=np.pi/6, vis=cfgs.vis)

    # Only predict in specific workspace range
    xmin, xmax = -0.19, 0
    ymin, ymax = -0.05, 0.15
    zmin, zmax = 0.0, 1.0
    lims = [xmin, xmax, ymin, ymax, zmin, zmax]
    demo_workspace_filtering(detector, points, colors, lims, vis=cfgs.vis)

    # You can also combine all the configurations
    object_id = 1
    gg = predict_with_configs(
        detector,
        points,
        region_steering=(seg_mask==object_id),
        approach_steering=[0,-1,0],
        approach_thresh=np.pi/18,
        dense_grasp=True,
        collision_detection=True,
    )
    if gg is not None and cfgs.vis:
        render_results(points, colors, gg)


if __name__ == '__main__':
    main('./example_data/')
