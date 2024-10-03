# Hello examples

This Markdown file contains examples of executable code blocks for various scripting languages. Use these examples to understand how to run code blocks with the runmd tool. Ensure that you have the appropriate interpreters installed on your machine before running these code blocks.

### Bash

```bash {name=hello-bash, tag=script}
# run with runmd run hello-bash
echo "Hello from bash!"
```

### Bash

```bash {name=hello-bash-prompt, tag=script}
# run with runmd run hello-bash
echo "Your name ?"
read name
echo "Hello $name !"
```


### hello-python

```python {name=hello-python}
# run with runmd run hello-python
print("Hello from Python!")
```

### hello-ruby

```ruby {name=hello-ruby}
# run with runmd run hello-ruby
puts "Hello from Ruby!"
```

### hello-perl

```perl {name=hello-perl}
# run with runmd run hello-perl
print "Hello from Perl!";
```

### hello-node

```javascript {name=hello-node}
// run with runmd run hello-node
console.log("Hello from JavaScript!");
```