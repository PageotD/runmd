`runmd` is built for ease of use with a simple, intuitive CLI. Get started with a few simple commands:

### Installation

```bash
pip install runmd
```

### Basic Usage

```bash
runmd run -f my_script.md -t python
```

- `runmd run` will execute all code blocks in your Markdown file.
- Use the `-t` option to run only specific tags like `python`, `bash`, etc.
  
### Viewing Code Blocks

```bash
runmd show -f my_script.md -t shell
```

- Quickly inspect code blocks with `runmd show`.
- Filter blocks by tag to narrow your focus.