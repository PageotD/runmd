# Docker example

Create a Dockerfile.apache containing the following;

```dockerfile
FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
```

Build image

```bash {name=docker-build-apache,tag=docker-example}
docker build -t my-apache2 -f dockerfile.apache .
```

Run image

```bash {name=docker-run-apache,tag=docker-example}
docker run -dit --name my-running-app -p 8080:80 my-apache2
```

```bash {name=docker-ps-apache,tag=docker-example}
docker ps -a
```

```bash {name=docker-stop-apache,tag=docker-example}
CONTAINER_ID=$(docker ps -aqf "name=my-running-app")
docker stop $CONTAINER_ID && docker rm $CONTAINER_ID
```