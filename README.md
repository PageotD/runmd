# RunMD: A CLI Tool for Executing Code Blocks in Markdown Files

RunMD is a command-line tool designed to extract and execute shell code blocks from Markdown files. This tool can be particularly useful for managing and running code snippets embedded in documentation or task lists.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6 or later
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

First, clone the repository to your local machine:

```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

Then install:
```sh
pip install .
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

#### Run a Specific Code Block

To execute a specific code block by name:

```sh
runmd run <code-block-name>
```