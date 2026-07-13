<img src="https://user-images.githubusercontent.com/12446953/208367719-4ef7922f-4001-41f7-aa9f-076e462d1325.png" width="60%">

# AnyGrasp SDK
AnyGrasp SDK for grasp detection & tracking.

[[arXiv](https://arxiv.org/abs/2212.08333)]
[[project](https://graspnet.net/anygrasp.html)]
[[dataset](https://graspnet.net/datasets.html)]
[[graspnetAPI](https://github.com/graspnet/graspnetAPI)]

## Update
* **July 13, 2026** We are testing the aarch64 version SDK. Try it out if you have interest. See the [dev](https://github.com/graspnet/anygrasp_sdk/tree/dev) branch for details.
* **July 4, 2026** We update AnyGrasp SDK with the following features:
  * Steer AnyGrasp using specific regions and approach vectors. This provides greater flexibility for task-oriented grasping and downstream manipulation tasks. See [USAGE.md](grasp_detection/USAGE.md) for details.
  * Added a new license tool. The previous `lib_cxx.so` and `license_checker` have been removed. Follow the [license instructions](license_registration/README.md) to apply for a license.
  * Added support for Python 3.14 and CUDA 13. See the [installation guide](#installation) for instructions on installing MinkowskiEngine with CUDA 13.
  * **Note: The old license tool is no longer supported.** License applications with old feature IDs submitted before July 4, 2026, will still be processed. Deployed machines can continue using the previous SDK. Please use the new license tool for the updated SDK.

* See [CHANGELOG.md](CHANGELOG.md) for historical updates.

## Video
[![IMAGE ALT TEXT](https://graspnet.net/images/broken.gif)](https://www.youtube.com/watch?v=s0SUw1vgtr8 "AnyGrasp Demo: Cleaning fragments of a broken pot")
<br>
**AnyGrasp cleaning fragments of a broken pot**


[![IMAGE ALT TEXT](https://user-images.githubusercontent.com/12446953/222949407-01a040d1-0723-4026-ae5a-08631116dde4.gif)](https://www.youtube.com/watch?v=2KM3Lq5VaS4 "AnyGrasp Fish Catching Spotlight")
<br>
**AnyGrasp catching swimming robot fish**

## Requirements
- Python 3.6-3.14
- PyTorch 1.7.1+ with CUDA 11.x/12.x/13.x
- [MinkowskiEngine](https://github.com/NVIDIA/MinkowskiEngine) v0.5.4


## Installation
1. Install [Pytorch](https://pytorch.org/get-started/locally/). Choose the appropriate version based on your environment.

2. Install MinkowskiEngine. We have modified MinkowskiEngine for better adpatation.
    ```bash
    mkdir dependencies && cd dependencies
    conda install openblas-devel -c anaconda
    export CUDA_HOME=/path/to/cuda
    git clone git@github.com:chenxi-wang/MinkowskiEngine.git
    cd MinkowskiEngine

    ## Uncomment the following line if you are using CUDA 12.x.
    # git checkout cuda-12-1

    ## Uncomment the following line if you are using CUDA 13.x.
    # git checkout cuda-13

    # Uncomment the following line if you are using CUDA 12.8+.
    ## The path of shared_ptr_base.h may change due to different OS versions, and you can locate the file path if it could not be found.
    ## For example, in Ubuntu 24.04, the path may be '/usr/include/c++/13/bits/shared_ptr_base.h'
    # sed -i 's/\bauto __raw = __to_address(__r.get());/auto __raw = std::__to_address(__r.get());/' /usr/include/c++/11/bits/shared_ptr_base.h

    python setup.py install --blas_include_dirs=${CONDA_PREFIX}/include --blas_library_dirs=${CONDA_PREFIX}/lib --blas=openblas
    cd ../..
    ```

3. Install other requirements from Pip.
    ```bash
    pip install -r requirements.txt
    ```

4. Install ``pointnet2`` module.
    ```bash
    cd pointnet2
    python setup.py install
    ```

5. Install graspnetAPI.
    ```bash
    git clone https://github.com/graspnet/graspnetAPI.git
    cd graspnetAPI
    pip install .
    ```

## License Registration
   
Due to the IP issue, currently we can only release the SDK library file of AnyGrasp in a licensed manner. Please get the feature id of your machine and fill in the [form](https://forms.gle/XVV3Eip8njTYJEBo6) to apply for the license. See [license_registration/README.md](license_registration/README.md) for details. **If you are interested in code implementation, you can refer to our [baseline version of network](https://github.com/graspnet/graspnet-baseline), or a third-party implementation of our [GSNet](https://github.com/graspnet/graspness_unofficial).**

We usually reply in 5 workdays. If you do not receive the reply in 5 workdays, **please check the spam folder.**


## Demo Code
Now you can run your code that uses AnyGrasp SDK. See [grasp_detection](grasp_detection) and [grasp_tracking](grasp_tracking) for details.


## Citation
Please cite these papers in your publications if it helps your research:

    @article{fang2023anygrasp,
      title={AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains},
      author = {Fang, Hao-Shu and Wang, Chenxi and Fang, Hongjie and Gou, Minghao and Liu, Jirong and Yan, Hengxu and Liu, Wenhai and Xie, Yichen and Lu, Cewu},
      journal={IEEE Transactions on Robotics (T-RO)},
      year={2023}
    }
    
    @inproceedings{fang2020graspnet,
      title={Graspnet-1billion: A large-scale benchmark for general object grasping},
      author={Fang, Hao-Shu and Wang, Chenxi and Gou, Minghao and Lu, Cewu},
      booktitle={Proceedings of the IEEE/CVF conference on computer vision and pattern recognition},
      pages={11444--11453},
      year={2020}
    }

    @inproceedings{wang2021graspness,
      title={Graspness discovery in clutters for fast and accurate grasp detection},
      author={Wang, Chenxi and Fang, Hao-Shu and Gou, Minghao and Fang, Hongjie and Gao, Jin and Lu, Cewu},
      booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
      pages={15964--15973},
      year={2021}
    }
