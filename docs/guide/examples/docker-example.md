# Interact with Docker

This example demonstrates how to build, run, and manage a simple Docker container using an Apache HTTP server. The steps cover Dockerfile creation, image building, container running, and stopping.

## Step 1: Create a Dockerfile

Start by creating a file named `Dockerfile.apache` with the following content. This file instructs Docker to use the official Apache HTTP server image and copy the contents of the `public-html` directory to the Apache document root.

```dockerfile
FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
```

## Step 2: Build and Run Docker Image

In this section, you will build the Docker image and run a container based on it.

### Build the Docker Image

The following command builds the Docker image using the `Dockerfile.apache` file. The image will be tagged as `my-apache2`.

```markdown
    ```bash {name=docker-build-apache,tag=docker-example}
    docker build -t my-apache2 -f Dockerfile.apache .
    ```
```

### Run the Docker Container

Once the image is built, you can run it as a container. The following command starts a container in detached mode, names it `my-running-app`, and exposes port `8080` on your local machine to port `80` on the container (the default Apache port).

```markdown
    ```bash {name=docker-run-apache,tag=docker-example}
    docker run -dit --name my-running-app -p 8080:80 my-apache2
    ```
```

You can now access the Apache server by navigating to `http://localhost:8080` in your web browser.

### List Docker Containers

To check the running containers, use the following command:

```markdown
    ```bash {name=docker-ps-apache,tag=docker-example}
    docker ps -a
    ```
```

This will list all Docker containers, including the one you've just started.

### Stop and Remove the Docker Container

When you're done, it's a good practice to stop and remove the container to free up resources. The following command stops and removes the container named `my-running-app`.

```markdown
    ```bash {name=docker-stop-apache,tag=docker-example}
    CONTAINER_ID=$(docker ps -aqf "name=my-running-app")
    docker stop $CONTAINER_ID && docker rm $CONTAINER_ID
    ```
```

## Full markdown file

!!! example "interact-with-docker.md"

    ```markdown
        # Interact with Docker

        ## Build the Docker Image

        The following command builds the Docker image using the `Dockerfile.apache` file. The image will be tagged as `my-apache2`.

        ```bash {name=docker-build-apache,tag=docker-example}
        docker build -t my-apache2 -f Dockerfile.apache .
        ```

        ## Run the Docker Container

        Once the image is built, you can run it as a container. The following command starts a container in detached mode, names it `my-running-app`, and exposes port `8080` on your local machine to port `80` on the container (the default Apache port).

        ```bash {name=docker-run-apache,tag=docker-example}
        docker run -dit --name my-running-app -p 8080:80 my-apache2
        ```

        You can now access the Apache server by navigating to `http://localhost:8080` in your web browser.

        ## List Docker Containers

        To check the running containers, use the following command:

        ```bash {name=docker-ps-apache,tag=docker-example}
        docker ps -a
        ```

        This will list all Docker containers, including the one you've just started.

        ## Stop and Remove the Docker Container

        When you're done, it's a good practice to stop and remove the container to free up resources. The following command stops and removes the container named `my-running-app`.

        ```bash {name=docker-stop-apache,tag=docker-example}
        CONTAINER_ID=$(docker ps -aqf "name=my-running-app")
        docker stop $CONTAINER_ID && docker rm $CONTAINER_ID
        ```
    ```