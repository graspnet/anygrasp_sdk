# AnyGrasp Detector Usage

AnyGrasp predicts parallel-jaw grasps from an unorganized 3D point cloud. The
main API consists of `create_detector(config)` for initialization and
`detector.get_grasp(points, optional_params)` for inference. We provide an brief introduction for the usage. You can also play with `demo.py` for in-depth application.

## Initialize the detector

```python
from argparse import Namespace
from gsnet import create_detector

# You can initialize the detector using argparse
config = Namespace(
    checkpoint_path="/path/to/checkpoint.tar",
    max_gripper_width=0.10,
    gripper_height=0.03,
)
# You can also initialize the detector using easy_dict
from easydict import EasyDict as edict
config = {
    "checkpoint_path": "/path/to/checkpoint.tar",
    "max_gripper_width": 0.10,
    "gripper_height": 0.03,
}
config = edict(config)

detector = create_detector(config)
if detector is None:
    raise RuntimeError("Failed to create detector")
```

### `create_detector(config)`

Input arguments:

| Argument | Data type | Description |
| --- | --- | --- |
| `config` | object with attributes | Detector configuration. An `argparse.Namespace` or `easydict.EasyDict` can be used. |
| `config.checkpoint_path` | `str` or path-like | Path to the model checkpoint. |
| `config.max_gripper_width` | `float` | Maximum accepted gripper opening in meters. It should be in `(0.0, 0.1]` |
| `config.gripper_height` | `float` | Gripper finger height in meters, assigned to every output grasp during collision detection. |

Output:

| Argument | Description |
| --- | --- |
| `detector` | Initialized detector when model loading and license validation succeed. `None` when license validation fails. |

## Predict grasps

```python
import numpy as np

# XYZ coordinates in meters
points = np.asarray(point_cloud_xyz, dtype=np.float32)  # shape (N, 3)

grasps = detector.get_grasp(points, {
    "dense_grasp": False,
    "collision_detection": True,
    "region_steering": None,
    "approach_steering": None,
    "approach_thresh": np.pi,
})

if grasps is not None:
    grasps = grasps.nms()
    grasps = grasps.sort_by_score()
    best_grasp = grasps[0]
```

### `detector.get_grasp(points, optional_params={})`

All steering coordinates use the same coordinate frame as `points`.

Input arguments:

| Argument | Data type | Default | Description |
| --- | --- | --- | --- |
| `points` | `numpy.ndarray`, shape `(N, 3)`, dtype `numpy.float32` | required | XYZ point cloud in meters. The SDK processes one point cloud per call. The point cloud should be in the camera coordinate frame. |
| `optional_params` | `dict[str, object]` | `{}` | Optional inference settings. Unknown keys are ignored. A non-dictionary value causes the method to return `None`. |
| `optional_params["dense_grasp"]` | `bool` | `False` | Generates denser predictions, potentially increasing coverage at the cost of prediction quality and runtime. `demo.py` skips NMS for dense output. |
| `optional_params["collision_detection"]` | `bool` | `True` | Filters grasp candidates that collide with the input point cloud. Disable it to retain more candidates without collision guarantees. |
| `optional_params["region_steering"]` | `numpy.ndarray`, shape `(N,)`, dtype `bool`, or `None` | `None` | Selects points in the desired object or workspace. Its length must equal the number of points. An all-false mask disables region steering. |
| `optional_params["approach_steering"]` | `list[float \| int]` or one-dimensional `numpy.ndarray`, shape `(3,)`, or `None` | `None` | Preferred 3D approach direction in the camera coordinate frame. The SDK normalizes it. A near-zero vector disables approach steering. |
| `optional_params["approach_thresh"]` | `float` or `int` | `numpy.pi` | Maximum angular deviation from the approach direction, in radians. Zero requests strict alignment; larger values allow a wider cone. |

Output:

| Argument | Data type | Description |
| --- | --- | --- |
| grasp_group | `graspnetAPI.GraspGroup` | Predicted grasps after width filtering and optional collision filtering. `None` if no grasp survived inference/filtering, or `optional_params` was invalid. |

Each grasp uses the GraspNet API representation:

| Field | Data type / shape | Description |
| --- | --- | --- |
| `score` | `float` | Confidence score; larger is better. |
| `width` | `float` | Required gripper opening in meters. |
| `height` | `float` | Gripper height in meters. |
| `depth` | `float` | Grasp insertion depth in meters. |
| `rotation_matrix` | `numpy.ndarray`, shape `(3, 3)` | Gripper orientation in the input point-cloud frame. |
| `translation` | `numpy.ndarray`, shape `(3,)` | Grasp center in meters in the input point-cloud frame. |
| `object_id` | `int` | Object identifier. AnyGrasp currently returns `-1`. |

Useful `GraspGroup` operations used by `demo.py`:

```python
grasps = grasps.nms()                           # suppress duplicate grasps
grasps = grasps.sort_by_score()                 # sort by descending confidence
top_20 = grasps[:20]                            # select the top 20
scores = top_20.scores                          # confidence score array
geometries = top_20.to_open3d_geometry_list()   # for open3d visualization
```

**Note 1: `translation` do not equal to the final gripper tip position.** The tip position should be computed using `translation`, `rotation_matrix` and `depth`:

```python
gripper_tip_position = translation + depth * rotation_matrix[:3, 0]
```

**Note 2: The gripper coordinate frames differ in different robots. Coordinate frame transformation may be required before execution.** The gripper frame used in graspnetAPI selects the approach direction as X-axis and the open/close direction Y-axis. You could refer to [graspnetAPI doc](https://graspnetapi.readthedocs.io/en/latest/grasp_format.html#d-grasp) for more details.

## Steering examples

### Region steering

The region steering mask must correspond element-for-element with `points`:

```python
object_id = 1
region_mask = segmentation_labels == object_id

grasps = detector.get_grasp(points, {
    "region_steering": region_mask,
    "dense_grasp": True,
    "collision_detection": True,
})
```

### Approach steering

The following accepts grasps within 60 degrees of the requested direction:

```python
grasps = detector.get_grasp(points, {
    "approach_steering": [0, 5, 1],
    "approach_thresh": np.pi / 3,
})
```

The vector does not need to be normalized. For top-down grasps in a frame where
positive Z is the desired approach direction, use `[0, 0, 1]`.

### Workspace filtering

Convert axis-aligned workspace limits to a region mask:

```python
xmin, xmax = -0.19, 0.0
ymin, ymax = -0.05, 0.15
zmin, zmax = 0.0, 1.0

workspace_mask = (
    (points[:, 0] >= xmin) & (points[:, 0] <= xmax) &
    (points[:, 1] >= ymin) & (points[:, 1] <= ymax) &
    (points[:, 2] >= zmin) & (points[:, 2] <= zmax)
)

grasps = detector.get_grasp(points, {
    "region_steering": workspace_mask,
})
```

All controls can be combined:

```python
grasps = detector.get_grasp(points, {
    "region_steering": region_mask,
    "approach_steering": [0, -1, 0],
    "approach_thresh": np.pi / 18,
    "dense_grasp": True,
    "collision_detection": True,
})
```

## Construct the point cloud from RGB-D data

`demo.py` projects a depth image into camera coordinates using the pinhole
camera model. Replace the intrinsics and depth scale with values from your
camera:

```python
depth_m = depth_image / depth_scale
u, v = np.meshgrid(
    np.arange(depth_image.shape[1]),
    np.arange(depth_image.shape[0]),
)

x = (u - cx) / fx * depth_m
y = (v - cy) / fy * depth_m
z = depth_m

valid = (z > 0) & (z < depth_truncation)
points = np.stack([x, y, z], axis=-1)[valid].astype(np.float32)
colors = rgb_image[valid].astype(np.float32) / 255.0
```

Only `points` is passed to the SDK. Colors are used for visualization, while
segmentation labels can be converted to `region_steering`.

## Run the demo
Run `demo.sh` to visualize the results or

```bash
python demo.py \
    --checkpoint_path /path/to/checkpoint.tar \
    --max_gripper_width 0.10 \
    --gripper_height 0.03 \
    --vis
```

| Command-line argument | Data type | Default | Description |
| --- | --- | --- | --- |
| `--checkpoint_path` | `str` | required | Model checkpoint path. |
| `--max_gripper_width` | `float` | `0.1` | Maximum gripper opening in meters, clamped by the demo to `[0.0, 0.1]`. |
| `--gripper_height` | `float` | `0.03` | Gripper height in meters. |
| `--vis` | `bool` flag | `False` | Opens Open3D windows for point-cloud and grasp visualization. |

The demo reads `color.png`, `depth.png`, and `seg_mask.png` from
`./example_data/`. Update the hard-coded camera intrinsics before using data
from another camera.
