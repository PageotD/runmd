<p align="center">
  <a href="">
    <img alt="RunMD Logo" src="./docs/static/runmd.svg" height="128" />
  </a>
  <h3 align="center">A CLI Tool for Executing Code Blocks in Markdown Files.</h3></br>
</p>


RunMD is a command-line tool designed to extract and execute code blocks from Markdown files. It's particularly useful for managing and running code snippets embedded in documentation or notes.

> **⚠** RunMD is intended for use with scripting languages only (e.g., Shell, Python, Ruby, JavaScript). It does not support compiled languages (e.g., C, C++, Java) as it cannot handle compilation and execution steps.
>
> **⚠** RunMD is different from interactive notebooks like [Jupyter](https://jupyter.org/) or [Zepplin](https://zeppelin.apache.org/). Each code block is independent and executed separately.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or later
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

### From Python Package Index
```console
pip install runmd
```

### From GitHub release

```console
pip install git+https://github.com/PageotD/runmd@0.10.1
```

### From source

Clone the GitHub repository:

```console
git clone https://github.com/PageotD/runmd.git
cd runmd
```

Install Build and Wheel Dependencies:
```console
pip install build wheel
```

Build and Install RunMD
```console
python -m build
pip install dist/runmd-<version>-py3-none-any.whl
```

## Initialize
```console
runmd init
```

## Usage

### Synopsis

```bash
runmd [COMMAND] [OPTIONS]
```

### Commands

**`RUN`**

Executes specified code blocks in a Markdown file.
```bash
runmd run [blockname] [--tag TAG] [--file FILE] [--env VAR=value ...]
```
* `blockname`: The name of the code block to run, or "all" to run all blocks.
* `-t [TAG], --tag [TAG]`: Specify the tag of the code blocks to run.
* `-f [FILE], --file [FILE]`: Specify the path to the Markdown file containing the code blocks.
* `--env VAR=value ...`: Optional environment variables to set during the execution.

</br>

**`SHOW`**

Displays the content of a specified code block.

```bash
runmd show [blockname] [--file FILE]
```

* `blockname`: The name of the code block to display.
* `-f [FILE], --file [FILE]`: Specify the path to the Markdown file.

</br>

**`LIST`**

Lists all the code blocks in a Markdown file.

```bash
runmd list [tag] [--file FILE]
```

* `-t [TAG], --tag [TAG]`: Optional tag to filter the list of code blocks.
* `-f [FILE], --file [FILE]`: Specify the path to the Markdown file.

</br>

**`HIST`**

Displays or clears the history of runmd commands.

```bash
runmd hist [id] [--clear]
```

* `id`: command line entry in history to execute.
* `--clear`: Clears definitely all the command line entries in history.

**`VAULT`**

Encrypt/Decrypt a markdown file using a password.

```console
runmd vault --encrypt README.md --outfile README.enc
```

```console
runmd vault --decrypt README.enc --outfile README.dec
```

* `-e [FILE], --encrypt [FILE]`: Encrypt the specified markdown file.
* `-d [FILE], --decrypt [FILE]`: Decrypt the encrypted file.
* `-o [FILE], --outfile [FILE]`: Optional output file name (default: add `.vault` suffix to input file name).

</br>

### Other options

Other options are quite standard:
* **`--help`**: to show the help message
* **`--version`**: to get the installed version of runmd

Display the version of 
### Add executable code block

To add an executable code block to your Markdown file, use the following syntax:

```markdown
# My executable code block
    ```sh {name=export-echo,tag=example}
    EXPORT MYSTR="a simple export and echo"
    echo $MYSTR
    ```
```

### List Code Blocks

To list all code block names in Markdown files within the current directory:

```console
runmd list
```

### Show a Specific Code Block
To display the content of a specific code block:

```console
runmd show <code-block-name>
```

### Run a Specific Code Block

To execute a specific code block by name:

```console
runmd run <code-block-name>
```

### Run all code blocks with a given tag

To execute a specific code block by name:

```console
runmd run -t <tag>
```

### Run all code blocks

To execute a specific code block by name:

```console
runmd run all
```

### Run a Specific Code Block with nvironment variable

To execute a specific code block by name:

```console
runmd run <code-block-name> --env <KEY1>=<VALUE1> <KEY2=VALUE2>
```

### Run all code blocks

To execute all code blocks in Markdown files within the current directory:

```console
runmd run all
```

## Configuration

You can customize how different scripting languages are executed by creating a configuration file at ~/.config/runmd/config.json. Here’s an example configuration:

```json
{
    "sh": {
        "command": "bash",
        "options": ["-c"]
    },
    "python": {
        "command": "python",
        "options": []
    },
    "ruby": {
        "command": "ruby",
        "options": []
    }
}
```

## Troubleshooting

* **No Output**: Ensure the Markdown code blocks are correctly formatted and the specified commands are valid for the environment.
* **Permission Denied**: Check if you have the required permissions to execute the commands in the code blocks.