# RunMD: A CLI Tool for Executing Code Blocks in Markdown Files

RunMD is a command-line tool designed to extract and execute code blocks from Markdown files. This tool can be particularly useful for managing and running code snippets embedded in documentation.

RunMD is developed in Python and use only modules from the Python's standard library, so there's no dependence on third-party modules.

> **⚠ RunMD is not a notebook like [Jupyter](https://jupyter.org/) or [Zepplin](https://zeppelin.apache.org/), each code block is independant from the others.**

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or later
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

### Using pip
...

### From sources
First, clone the repository to your local machine:

```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

Then install:
```sh
python setup.py sdist
pip install sdist/runmd-0.1.0.tar.gz
```


### Usage


After installing the tool, you can use the `runmd` command to interact with your Markdown files.

#### Add executable code block

To add an executable `sh` code block to your markdown file

```markdown
# My executable code block
    ```sh {name=export-echo}
    EXPORT MYSTR="a simple export and echo"
    echo $MYSTR
    ```
```

#### List Code Blocks

To list all code block names in Markdown files within the current directory and subdirectories:

```sh
runmd ls
```

#### Show a Specific Code Block
To show a specific code block in terminal

```sh
runmd show <code-block-name>
```

#### Run a Specific Code Block

To execute a specific code block by name:

```sh
runmd run <code-block-name>
```

#### Run all code blocks

```sh
runmd run all
```