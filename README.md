# AnyGrasp SDK
AnyGrasp SDK for grasp detection & tracking.

[[publication](https://graspnet.net/publications.html)]
[[dataset](https://graspnet.net/datasets.html)]
[[graspnetAPI](https://github.com/graspnet/graspnetAPI)]


## Requirements
- Python 3.6/3.7/3.8/3.9
- PyTorch 1.7.1 with CUDA 11.0
- [MinkowskiEngine](https://github.com/NVIDIA/MinkowskiEngine) v0.5.4


## Installation
1. Follow MinkowskiEngine [instructions](https://github.com/NVIDIA/MinkowskiEngine#anaconda) to install [Anaconda](https://www.anaconda.com/), cudatoolkit, Pytorch and MinkowskiEngine. **Note that you need ``export MAX_JOBS=2;`` before ``pip install`` due to [this issue](https://github.com/NVIDIA/MinkowskiEngine/issues/228)**. If PyTorch reports a compatibility issue during program execution, you can re-install PyTorch via Pip instead of Anaconda.

2. Install other requirements from Pip.
```bash
    pip install -r requirements.txt
```

3. Install ``pointnet2`` module.
```bash
    cd pointnet2
    python setup.py install
```

## License Registration
   
Get the feature id of your machine and fill in the [chart]() to apply for license. See [license_registration/README.md](license_registration/README.md) for details.


## Demo
Now you can run your code that uses AnyGrasp SDK. See [grasp_detection](grasp_detection) and [grasp_tracking](grasp_tracking) for details.