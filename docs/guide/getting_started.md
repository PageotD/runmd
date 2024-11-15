`runmd` is built for ease of use with a simple, intuitive CLI. Get started with a few simple commands:

!!! warning "MS Windows Systems"
    For Windows users, it is preferable to use Windows Subsystem for Linux 2 (WSL 2) . There is currently no support for MS Windows systems, although the python package should install and run correctly.

### Installation from pip

The easiest way to install `RunMD` on UNIX-like system is by using `pip` (the Package Installer for Python).
First, make sure you have Python and that the expected version (3.9 to 3.12) is available from your command line. You can check this by running:

```bash
python3 --version
```

Ensure you have pip available. You can check this by running:

```bash
python3 -m pip --version
```

Finally, you install the latest version of `RunMD` by running:
```bash
python3 -m pip install runmd
```

### Install from GitHub release

In the case of GitHub-hosted release installation, the procedure is similar to that described in the previous section. The difference lies in the pip command, where you'll need to specify the version you wish to install (replace `<version>` with the desired version, e.g. 0.15.0):

```bash
python3 -m pip install git+https://github.com/PageotD/runmd@<version>
```

### Installation from source

To build from source you must install `build` and `wheel` packages.
```bash
pip install build whell
```

Clone the git repository
```bash
git clone git@github.com:PageotD/runmd.git
```

Build and install
```bash
python -m build && pip install dist/runmd*.whl
```