# ENV EXAMPLE

```sh {name=env-example}
# runmd run env-example --env MSG="Hello world from env!"
echo $MSG
```

```sh {name=docker-example}
IMAGE_NAME="test-runmd"
cd examples/
ls -al Dockerfile
echo "Build Docker image"
docker build -t $IMAGE_NAME .
cd -
echo "Get image ID"
docker images -q $IMAGE_NAME
```
