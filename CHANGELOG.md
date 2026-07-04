# AnyGrasp SDK Change Log

* **July 4, 2026** We update AnyGrasp SDK with the following features:
  * Steer AnyGrasp using spcific regions and approach vectors. This provides greater flexibility for task-oriented grasping and downstream manipulation tasks. See [USAGE.md](grasp_detection/USAGE.md) for details.
  * Added a new license tool. The previous `lib_cxx.so` and `license_checker` have been removed. Follow the [license instructions](license_registration/README.md) to apply for a license.
  * Added support for Python 3.14 and CUDA 13. See the [installation guide](#installation) for instructions on installing MinkowskiEngine with CUDA 13.
  * **Note: The old license tool is no longer supported.** License applications with old feature IDs submitted before July 4, 2026, will still be processed. Deployed machines can continue using the previous SDK. Please use the new license tool for the updated SDK.

* **June 10, 2026** We are testing AnyGrasp steering and a new license tool, where lib_cxx.so and license_checker are removed and Python 3.14 is supported. There are slight changes in API and feature id generation. **The current version will be replaced in one month.** If you need no updates for the deployed machines in the future, you do not need to apply for a new license. We are also planning to support aarch64 in the future. Help us test the new version if you are interested!

* **November 23, 2025** Support CUDA 12.8 and Python 3.11/3.12/3.13.

* **August 1, 2024** Support Python 3.10.

* **May 7, 2024** Add new features and flags to AnyGrasp detector:
  * Dense Predictions (default is False)
    * Set ``dense_grasp=True`` to enable extremely dense output. It's helpful for some corner cases or prompt-based grasping.
    * **Warning: this mode is designed for special scenarios, leading to higher GPU memory, lower inference speed and lower grasp quality. You can crop the point clouds with your own segmantation masks or 3D bounding boxes to improve the performance.**
  * Filtering by Objectness Mask (default is True)
    * Set ``apply_object_mask=False`` to disable default grasp filtering by objectness masks. This will lead to predictions on backgrounds.
  * Collision Detection (default is True)
    * Set ``collision_detection=False`` to disable default collision detection step.
  * These flags are useful for more flexible development, but **we highly recommend to use the default setting in common scenarios**. See [grasp_detection/demo.py](grasp_detection/demo.py) for examples.

* **October 8, 2023** Fix a bug in grasp detection inference code, which may cause partial grasp widths exceeding the constrained range.

* **July 20, 2023** Fix a bug in grasp detection inference code, which may cause no prediction when there are only one or two objects.