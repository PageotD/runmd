---
hide:
  - navigation
  - toc
---

RunMD is a command-line tool designed to extract and execute code blocks from Markdown files. It's particularly useful for managing and running code snippets embedded in documentation or notes.

> **⚠** RunMD is intended for use with scripting languages only (e.g., Shell, Python, Ruby, JavaScript). It does not support compiled languages (e.g., C, C++, Java) as it cannot handle compilation and execution steps.
>
> **⚠** RunMD is different from interactive notebooks like [Jupyter](https://jupyter.org/) or [Zepplin](https://zeppelin.apache.org/). Each code block is independent and executed separately.

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`runmd`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Getting started](guide/getting_started.md)

</div>

!!! getting-started note ""

    <figure markdown="1">
    <h1><b>Open source, MIT License, Python 3.9 to 3.12 with minimal dependencies</b></h1>
    [Getting started](guide/getting_started.md){ .md-button .getting_started }
    </figure>


<div style="margin: 0 auto; padding: 10px 20px; width: 80%; max-width: 750px;text-align: center; border: 1px solid; border-radius: 5px; border-color: #ff6f00ff; display: flex; align-items: center; justify-content: space-between;">
  <div style="width: 65%; font-size: 1.5em; text-align: left;">
    Open source, MIT License, Python 3.9 to 3.12 with minimal dependencies
  </div>
  <div style="width: 25%; font-size: 1.5em; text-align: right;">
    <img src="./static/github-mark.svg" />
  </div>
</div>

## Key Features

- **Run code blocks**: Execute code blocks directly from your Markdown files with a simple command.
- **View code blocks**: List and display code blocks, helping you manage and organize your scripts.
- **Tag filtering**: Run or display blocks based on tags for organized and targeted execution.
- **Command history**: Keep track of your executed commands and even re-run them at will.

## Why `runmd`?

Whether you're documenting your code, preparing interactive tutorials, or keeping a technical journal, `runmd` gives you the power to:

- :material-folder-open-outline:{ .orange }  **Stay organized**: Keep all your scripts and examples in one Markdown file without the hassle of jumping between files.
- :material-rocket-launch:{ .orange }  **Increase productivity**: No more copy-pasting code. Just define and run code blocks within the same document.
- :material-sync:{ .orange }  **Maintain consistency**: Run code in different environments while ensuring outputs and behavior are documented right next to the source.


