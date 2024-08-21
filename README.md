# RunMD: A CLI Tool for Executing Code Blocks in Markdown Files

RunMD is a command-line tool designed to extract and execute code blocks from Markdown files. It's particularly useful for managing and running code snippets embedded in documentation or notes.

> **⚠** RunMD is intended for use with scripting languages only (e.g., Shell, Python, Ruby, JavaScript). It does not support compiled languages (e.g., C, C++, Java) as it cannot handle compilation and execution steps.
>
> **⚠** RunMD is different from interactive notebooks like [Jupyter](https://jupyter.org/) or [Zepplin](https://zeppelin.apache.org/). Each code block is independent and executed separately.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or later
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

### 1. Clone the repository to your local machine:

```sh {name=runmd-clone}
git clone https://github.com/PageotD/runmd.git
cd runmd
```

### 2. Install Build Dependencies
```sh {name=runmd-pip}
pip install build
```

### 3. Build and Install RunMD
```sh {name=runmd-build-install}
python -m build
pip install dist/runmd-<version>-py3-none-any.whl
```

### 4. Initialize
```sh {name=runmd-initialize}
runmd init
```

## Usage

Once installed, you can use the runmd command to interact with your Markdown files.

| Command | Description |
|------|------|
| run | Run a selected code block |
| show | Print the content of the selected code block |
| list | List available code blocks |

| Flag | Description |
|------|------|
| --file | Name of the markdown file to work with |
| --env | Pass environment variables |

### Synopsis

```bash
runmd [COMMAND] [OPTIONS]
```

### Commands

**`RUN`**

Executes specified code blocks in a Markdown file.
```bash
runmd run [blockname] [--file FILE] [--env VAR=value ...]
```
* `blockname`: The name of the code block to run, or "all" to run all blocks.
* `--file FILE`: Specify the path to the Markdown file containing the code blocks.
* `--env VAR=value ...`: Optional environment variables to set during the execution.

</br>

**`SHOW`**

Displays the content of a specified code block.

```bash
runmd show [blockname] [--file FILE]
```

* `blockname`: The name of the code block to display.
* `--file FILE`: Specify the path to the Markdown file.

</br>

**`LIST`**

Lists all the code blocks in a Markdown file.

```bash
runmd list [tag] [--file FILE]
```

* `tag`: Optional tag to filter the list of code blocks.
* `--file FILE`: Specify the path to the Markdown file.

</br>

**`HIST`**

Displays or clears the history of runmd commands.

```bash
runmd hist [--clear]
```

* `--clear`: Clears the stored command history.

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

```sh
runmd list
```

### Show a Specific Code Block
To display the content of a specific code block:

```sh
runmd show <code-block-name>
```

### Run a Specific Code Block

To execute a specific code block by name:

```sh
runmd run <code-block-name>
```

### Run all code blocks with a given tag

To execute a specific code block by name:

```sh
runmd run @<tag>
```

### Run all code blocks

To execute a specific code block by name:

```sh
runmd run all
```

### Run a Specific Code Block with nvironment variable

To execute a specific code block by name:

```sh
runmd run <code-block-name> --env <KEY1>=<VALUE1> <KEY2=VALUE2>
```

### Run all code blocks

To execute all code blocks in Markdown files within the current directory:

```sh
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