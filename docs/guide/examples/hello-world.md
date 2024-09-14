# Hello World with RunMD

Welcome to the RunMD introduction guide! In this document, we'll walk you through how to use RunMD to execute code blocks in different languages from within a Markdown file.

To get started with RunMD, you'll need to create a Markdown file containing your code blocks.

## Create a runnable code block

A runnable code block is like any other code block in Markdown except it has some extra attributes. 

```markdown
    ```<script language> {name=<block name>,tag=<optional tag>}
    # some stuff...
```

The `name` attribute is mandatory, it allows RunMD to determine if it is a runnable code block.

The `tag` attribute is optional, it allows to run group of code blocks.

!!! example "hello-examples.md"

    ```markdown
        # Hello examples

        Using bash

        ```bash {name=hello-bash,tag=hello-examples}
        echo "Hello from bash!"
        ```

        Using python

        ```python {name=hello-python,tag=hello-examples}
        print("Hello from python!")
        ```

        Using nodejs
        ```node {name=hello-node,tag=hello-examples}
        console.log("Hello from JavaScript!");
        ```
    ```

## List your code blocks

```bash
runmd list
```

...output...

```console
NAME                           LANG            FILE                                     TAG            
-------------------------------------------------------------------------------------------------------
hello-python                   python          tests/test_markdown.md                   sometag        
hello-ruby                     ruby            tests/test_markdown.md                                  
geo-json                       python          examples/advanced-examples.md            geoloc         
geo-dist                       python          examples/advanced-examples.md            geoloc
```

## Show code block in terminal

```bash
runmd show <code block name>
```

...output...

```console

    | # run with runmd run hello-python
    | print("Hello from Python!")

```

!!! note

    If you have [`Pygments`](https://pygments.org/) package installed, the output will appear with syntax highlighting. You can install `Pygments` with:
    ```bash
    pip install pygments
    ```

## Run code block by name

```bash
runmd run <code block name>
```

...output...

```console
> Running: hello-python (python) hello-examples
Hello from Python!
```

## Run code blocks by tag

```bash
runmd run -t <tag name>
```

...output...