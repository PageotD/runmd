# Simple examples

#### sys-info
```sh {name=sys-info}
echo "System Information:"
uname -a
echo "Disk Usage:"
df -h
echo "Memory Usage:"
free -h
```

#### ping-test
```sh {name=ping-test}
echo "Pinging google.com..."
ping -c 4 google.com
```

#### process-list
```sh {name=process-list}
echo "Listing running processes:"
ps aux
```

### hello-bash
```sh {name=hello-bash}
echo "Hello from bash!"
```

### hello-python

```python {name=hello-python}
print("Hello from Python!")
```

### hello-ruby
```ruby {name=hello-ruby}
puts "Hello from Ruby!"
```

### hello-perl
```perl {name=hello-perl}
print "Hello from Perl!";
```

### hello-node
```javascript {name=hello-node}
console.log("Hello from JavaScript!");
```

### python-quadratic
```python {name=python-quadratic}
# Solve the quadratic equation ax**2 + bx + c = 0

# import complex math module
import cmath

a = 1
b = 5
c = 6

# calculate the discriminant
d = (b**2) - (4*a*c)

# find two solutions
sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)

print('The solution are {0} and {1}'.format(sol1,sol2))
```

### python-add-matrices
```python {name=python-add-matrices}
# Program to add two matrices using nested loop

X = [[12,7,3],
    [4 ,5,6],
    [7 ,8,9]]

Y = [[5,8,1],
    [6,7,3],
    [4,5,9]]

result = [[0,0,0],
         [0,0,0],
         [0,0,0]]

# iterate through rows
for i in range(len(X)):
   # iterate through columns
   for j in range(len(X[0])):
       result[i][j] = X[i][j] + Y[i][j]

for r in result:
   print(r)
```