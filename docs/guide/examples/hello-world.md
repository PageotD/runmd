# Hello World with RunMD

Welcome to the `RunMD` introduction guide! This guide will teach you how to use `RunMD` to execute code blocks in different programming languages directly from Markdown files. By embedding runnable code in your documentation, you can bring your Markdown files to life—ideal for tutorials, demonstrations, or dynamic workflows.

---

## Create a Runnable Code Block

A runnable code block in `RunMD` is similar to a standard Markdown code block but includes additional attributes to make it executable. These attributes allow `RunMD` to identify and organize code blocks.

### Syntax Overview

The syntax for a runnable code block is:

```markdown
    ```<language> {name=<unique_block_name>, tag=<optional_group_tag>}
    # Code goes here...
    ```
```

- **`<language>`**: Specify the programming language (e.g., `python`, `bash`, `node`, `ruby`, `perl`).
- **`name`**: A **required** attribute that provides a unique identifier for the code block.
- **`tag`**: An **optional** attribute to group related blocks under a shared tag for batch execution.

### Example Markdown File

Here’s an example Markdown file (`hello-examples.md`) that defines runnable code blocks in multiple programming languages:

!!! example "hello-examples.md"

    ```markdown
        # Hello Examples

        Using Bash:

        ```bash {name=hello-bash, tag=hello-examples}
        # Execute with: runmd run hello-bash
        echo "Hello from Bash!"
        ```

        Using Python:

        ```python {name=hello-python, tag=hello-examples}
        # Execute with: runmd run hello-python
        print("Hello from Python!")
        ```

        Using Node.js:

        ```node {name=hello-node, tag=hello-examples}
        // Execute with: runmd run hello-node
        console.log("Hello from Node.js!");
        ```

        Using Ruby:

        ```ruby {name=hello-ruby, tag=hello-examples-2}
        # Execute with: runmd run hello-ruby
        puts "Hello from Ruby!"
        ```

        Using Perl:

        ```perl {name=hello-perl, tag=hello-examples-2}
        # Execute with: runmd run hello-perl
        print "Hello from Perl!";
        ```
    ```

In this example:

- Each block has a unique `name` (e.g., `hello-bash`, `hello-python`).
- The `tag` attribute groups the blocks (e.g., `hello-examples` for Python, Bash, and Node.js).

---

## List Your Code Blocks

Once you’ve created a Markdown file with runnable blocks, you can use the `list` command to view all available blocks. This is especially useful for verifying block names and tags.

```bash
runmd list
```

### Example Output

```console
$ runmd list
NAME              LANG        FILE                 TAG               
-------------------------------------------------------------------
hello-bash        bash        hello-examples.md    hello-examples  
hello-python      python      hello-examples.md    hello-examples  
hello-node        node        hello-examples.md    hello-examples  
hello-ruby        ruby        hello-examples.md    hello-examples-2
hello-perl        perl        hello-examples.md    hello-examples-2
```

### Explanation of Columns:
- **NAME**: The unique name of the code block.
- **LANG**: The programming language of the block.
- **FILE**: The file where the block is defined.
- **TAG**: The optional tag associated with the block.

---

## Show a Code Block in the Terminal

To preview the content of a specific code block, use the `show` command with the block’s name:

```bash
runmd show <code block name>
```

### Example

```bash
runmd show hello-bash
```

### Output

```console
$ runmd show hello-bash

    | # Execute with: runmd run hello-bash
    | echo "Hello from Bash!"
```

This feature is useful for confirming the exact code before execution.

!!! note
    If you have the [`Pygments`](https://pygments.org/) package installed, the output will include syntax highlighting. Install it using:
    ```bash
    pip install pygments
    ```

---

## Run a Code Block by Name

To execute a specific code block, use the `run` command with the block’s unique name:

```bash
runmd run <code block name>
```

### Example

```bash
runmd run hello-python
```

### Output

```console
$ runmd run hello-python

> Running: hello-python (python) hello-examples
Hello from Python!
```

Here, `RunMD` automatically detects the language, runs the block, and displays the output.

---

## Run Code Blocks by Tag

If you want to execute multiple code blocks together, group them using the `tag` attribute and run them with the `-t` option:

```bash
runmd run -t <tag name>
```

### Example

```bash
runmd run -t hello-examples-2
```

### Output

```console
$ runmd run -t hello-examples-2

> Running: hello-ruby (ruby) hello-examples-2
Hello from Ruby!

> Running: hello-perl (perl) hello-examples-2
Hello from Perl!
```

### Why Tags?

Tags allow you to organize related blocks, enabling batch execution without specifying each block by name. This is particularly useful for workflows with multiple interdependent steps.
