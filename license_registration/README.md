# License Registration

- Get the feature id of your working machine directly using the SDK. The format of the feature id should be "N12345678900987654321".
    ```base
    cp ../grasp_detection/gsnet_versions/gsnet.cpython-36m-x86_64-linux-gnu.so gsnet.so
    python -c "from gsnet import get_feature_id; print(get_feature_id())"
    ```
- Fill in the [form](https://forms.gle/XVV3Eip8njTYJEBo6) to apply for license, which requires the machine feature id. **Note: if there is a "%" at the end of the machine id, delete it when filling the form.**
- You will get a `.zip` file that contains license. The folder structure is as follows (see [sample_license](sample_license) for example):
    ```base
    license/
    |-- licenseCfg.json
    |-- [your_name].public_key
    |-- [your_name].signature
    |-- [your_name].lic
    ```
- To validate your license, unzip and put your license folder here as "license", and run
    ```base
    python -c "from gsnet import check_license; check_license('license')"
    ```
- Put the license folder under [grasp_detection](../grasp_detection) and [grasp_tracking](../grasp_tracking) to execute the demo.
