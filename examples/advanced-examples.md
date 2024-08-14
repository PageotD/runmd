# Advanced examples

## Create a JSON file with geolocation data

```python {name=geo-json, tag=geoloc}
import json

geoloc = {
    "lat1": 47.2734,
    "lon1": -2.2138,
    "lat2": 47.0864,
    "lon2": -1.2804
}

with open("geoloc.json", "w") as f:
    f.write(json.dumps(geoloc, indent=2))
print("geoloc.json file created")
```

Check file

```sh {name=geo-check, tag=geoloc}
ls -l geoloc.json
```

## Distance between two geolocalisation points

Need to run the prvious code block before.

```python {name=geo-dist, tag=geoloc}
import json
from math import radians, sin, cos, acos
 
with open("geoloc.json", "r") as f:
    geoloc = json.load(f)

mlat = radians(geoloc["lat1"])
mlon = radians(geoloc["lon1"])
plat = radians(geoloc["lat2"])
plon = radians(geoloc["lon2"])
 
dist = 6371.01 * acos(sin(mlat)*sin(plat) + cos(mlat)*cos(plat)*cos(mlon - plon))
print("The distance is %.2fkm." % dist)
```

## Fibonacci Sequence

```python {name=fibonacci}
# runmd run fibonacci --env NFIBO=9
import os

def Fibonacci(n):

	# Check if input is 0 then it will
	# print incorrect input
	if n < 0:
		print("Incorrect input")

	# Check if n is 0
	# then it will return 0
	elif n == 0:
		return 0

	# Check if n is 1,2
	# it will return 1
	elif n == 1 or n == 2:
		return 1

	else:
		return Fibonacci(n-1) + Fibonacci(n-2)

# Get nfibo from environment variable NFIBO
nfibo = int(os.environ["NFIBO"])
print(Fibonacci(nfibo))
```