# License Registration

- Get the feature id of your working machine.
```base
    ./license_checker -f
```
- Name a discriminator for the usage, such as device serial number, or collaborator's name.
- Fill in the [chart]() to apply for license, which requires both feature id and discriminator.
- You will get a `.zip` file that contains license with time limitation. The folder structure is as follows (see [sample_license](sample_license) for example):
```base
    license/
       |-- licenseCfg.json
       |-- [discriminator].public_key
       |-- [discriminator].signature
       |-- [discriminator].lic
```
- You can check license states via
```base
    ./license_checker -c license/licenseCfg.json
```
- Now you can run your code that uses AnyGrasp SDK. See [grasp_detection](../grasp_detection) and [grasp_tracking](../grasp_tracking) for details.