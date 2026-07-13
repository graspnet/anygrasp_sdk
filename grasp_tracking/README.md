# AnyGrasp Tracking Demo
This demo shows the usage of AnyGrasp tracking SDK. Note that `tracker.so` and license files are required for execution and both binary files have different Python versions.

## Instruction
1. Copy `tracker.*.so` to this folder based on your architecture (x86_64/aarch64) and Python version (>=3.6). For example, if you use x86_64 and Python 3.6, you can do as follows:
```bash
    cp tracker_versions/x86_64/tracker.cpython-36m-x86_64-linux-gnu.so tracker.so
```

2. Unzip your license and put the folder here as `license`. Refer to [license_registration/README.md](../license_registration/README.md) if you have not applied for license.

3. Put model weights under ``log/``.

## Execution

Run your code like `demo.py` or any desired applications that uses `tracker.so`. See `demo.py` for more details.
```bash
    sh demo.sh
```