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

        Using Bash

        ```bash {name=hello-bash,tag=hello-examples}
        # run with runmd run hello-bash
        echo "Hello from bash!"
        ```

        Using Python

        ```python {name=hello-python,tag=hello-examples}
        # run with runmd run hello-python
        print("Hello from python!")
        ```

        Using NodeJS

        ```node {name=hello-node,tag=hello-examples}
        // run with runmd run hello-node
        console.log("Hello from nodejs!");
        ```

        Using Ruby

        ```ruby {name=hello-ruby,tag=hello-examples-2}
        # run with runmd run hello-ruby
        puts "Hello from Ruby!"
        ```

        Using Perl

        ```perl {name=hello-perl, tag=hello-examples-2}
        # run with runmd run hello-perl
        print "Hello from Perl!";
        ```
    ```

## List your code blocks

```bash
runmd list
```

...output...

```console
$ runmd list
NAME                           LANG            FILE                                     TAG            
-------------------------------------------------------------------------------------------------------
hello-bash                     bash            hello-examples.md                        hello-examples 
hello-python                   python          hello-examples.md                        hello-examples 
hello-node                     node            hello-examples.md                        hello-examples 
hello-ruby                     ruby            hello-examples.md                        hello-examples-2
hello-perl                     perl            hello-examples.md                        hello-examples-2
```

## Show code block in terminal

```bash
runmd show <code block name>
```

```console
$ runmd show hello-bash

    | # run with runmd run hello-bash
    | echo "Hello from bash!"

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

```console
$ runmd run hello-python

> Running: hello-python (python) hello-examples
Hello from python!
```

## Run code blocks by tag

```bash
runmd run -t <tag name>
```

```console
$runmd run -t hello-examples-2

> Running: hello-ruby (ruby) hello-examples-2
Hello from Ruby!

> Running: hello-perl (perl) hello-examples-2
Hello from Perl!
```