# AnyGrasp Detection Demo
This demo shows the usage of AnyGrasp detection SDK. Note that `gsnet.so` and license files are required for execution and both binary files have different Python versions.

## Instruction
1. Copy `gsnet.*.so` to this folder according to your Python version (Python>=3.6 is supported). For example, if you use Python 3.6, you can do as follows:
```bash
    cp gsnet_versions/gsnet.cpython-36m-x86_64-linux-gnu.so gsnet.so
```

2. Unzip your license and put the folder here as `license`. Refer to [license_registration/README.md](../license_registration/README.md) if you have not applied for license.

3. Put model weights under ``log/``.

## Execution

Run your code like `demo.py` or any desired applications that uses `gsnet.so`. See `demo.py` for more details.
```bash
    sh demo.sh
```