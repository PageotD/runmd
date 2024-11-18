`runmd` is built for ease of use with a simple, intuitive CLI. Get started with a few simple commands:

!!! warning "MS Windows Systems"
    For Windows users, it is preferable to use Windows Subsystem for Linux 2 (WSL 2) . There is currently no support for MS Windows systems, although the python package should install and run correctly.

## Prerequistes

Before installing `RunMD, ensure that you have:
- Python (version 3.9 to 3.12)
- pip (the Python package installer)

Verify your Python installation by running:
```bash
python3 --version
```

Ensure pip is installed:
```bash
python3 -m pip --version
```

If Python or pip is not installed, please refer to the official [Python documentation](https://www.python.org/downloads/) for installation instructions.

## Installation via PyPi

The easiest way to install `RunMD` on UNIX-like system is by using `pip`:
```bash
python3 -m pip install runmd
```

To upgrade to the lastest version:
```bash
python3 -m pip install --upgrade runmd
```

## Installation from GitHub Release

If you prefer to install a specific version directly from the GitHub repository, use the following command. Replace <version> with the desired version (e.g., 0.15.0):

```bash
python3 -m pip install git+https://github.com/PageotD/runmd@<version>
```
You can find a list of available versions on the [GitHub Release page](https://github.com/PageotD/runmd/releases).

## Installation from Source

To build and install `RunMD` from the source code, follow these steps:

1. **Install Build Tools**

    Ensure you have the necessary build tools installed:
    ```bash
    python3 -m pip install build wheel
    ```

2. **Clone the Repository**

    Clone the `RunMD` repository from GitHub:
    ```bash
    git clone https://github.com/PageotD/runmd.git
    cd runmd
    ```  

3. **Build and Install**

    Build the package and install it locally:
    ```bash
    python3 -m build
    python3 -m pip install dist/runmd-*.whl
    ```      

## Verifying the Installation

After installation, verify that RunMD is correctly installed by running:
```bash
runmd --version
```