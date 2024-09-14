---
hide:
  - navigation
  - toc
---

RunMD is a command-line tool designed to extract and execute code blocks from Markdown files. It's particularly useful for managing and running code snippets embedded in documentation or notes.

> **⚠** RunMD is intended for use with scripting languages only (e.g., Shell, Python, Ruby, JavaScript). It does not support compiled languages (e.g., C, C++, Java) as it cannot handle compilation and execution steps.
>
> **⚠** RunMD is different from interactive notebooks like [Jupyter](https://jupyter.org/) or [Zepplin](https://zeppelin.apache.org/). Each code block is independent and executed separately.

<div class="grid cards" style="grid-template-columns: repeat(3, 1fr); margin: 0 auto; padding: 10px 20px; width: 80%; gap: 32px;" markdown>

  - :material-timer-outline:{ .lg .middle .orange } __Set up in minute__

    ---
  
    Install [`runmd`](#) with [`pip`](#) and get up
    and running in minute

    [:material-arrow-right: Getting started](guide/getting_started.md)

  - :simple-markdown:{ .lg .middle .orange } __Only Markdown__
  
    ---
  
    Gather scripts and documentation in one Markdown file

    [:material-arrow-right: See examples](#)

  - :material-license:{ .lg .middle .orange } __Open Source__
  
    ---
  
    RunMD is licensed under the MIT license and is available on [GitHub](https://github.com/PageotD/runmd)

    [:material-arrow-right: License](infos/LICENSE.md)

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


