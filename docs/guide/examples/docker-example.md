# Interact with Docker

This guide walks you through building, running, and managing a simple Docker container that uses an Apache HTTP server. By following these steps, you’ll learn how to:

- Create a `Dockerfile` for defining your container image.
- Build the Docker image.
- Run a container from the image and access its services.
- List, stop, and clean up Docker containers.

---

## Step 1: Create a Dockerfile

A `Dockerfile` is a script-like file that contains a series of instructions for building a Docker image. Create a file named `Dockerfile.apache` with the following content:

```dockerfile
FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
```

### Explanation:

- **`FROM httpd:2.4`**: This specifies the base image to use, which is version `2.4` of the official Apache HTTP server image.
- **`COPY ./public-html/ /usr/local/apache2/htdocs/`**: This copies the content of your local `public-html` directory into the Apache document root directory inside the container (`/usr/local/apache2/htdocs/`).

---

## Step 2: Build and Run the Docker Image

Now that your `Dockerfile` is ready, you’ll proceed to build the image and start a container.

### Build the Docker Image

Use the following command to build the Docker image. The `-t` option assigns a name (`my-apache2`) to your image, and the `-f` option specifies the `Dockerfile.apache` file to use.

```markdown
    ```bash {name=docker-build-apache,tag=docker-example}
    docker build -t my-apache2 -f Dockerfile.apache .
    ```
```

This command reads the `Dockerfile.apache`, processes its instructions, and creates a Docker image named `my-apache2`.

### Run the Docker Container

With the image built, you can now create and start a container. The following command starts a container in detached mode:

```markdown
    ```bash {name=docker-run-apache,tag=docker-example}
    docker run -dit --name my-running-app -p 8080:80 my-apache2
    ```
```

#### What this does:
- **`-dit`**: Runs the container in detached mode (`-d`) and interactive mode (`-i`) with a TTY (`-t`).
- **`--name my-running-app`**: Assigns the container a name (`my-running-app`) for easier management.
- **`-p 8080:80`**: Maps port `8080` on your local machine to port `80` on the container (the default Apache HTTP port).
- **`my-apache2`**: Specifies the Docker image to use.

Once the container is running, open a web browser and navigate to `http://localhost:8080` to view your Apache HTTP server in action.

---

## Step 3: Manage Docker Containers

Docker provides commands to list, stop, and remove containers. Here’s how you can manage the container you’ve just started.

### List Docker Containers

To view all containers (both running and stopped), use:

```markdown
    ```bash {name=docker-ps-apache,tag=docker-example}
    docker ps -a
    ```
```

#### Example Output:

```console
$ docker ps -a
CONTAINER ID   IMAGE       COMMAND              STATUS              PORTS                  NAMES
123456abcd     my-apache2  "httpd-foreground"   Up 2 minutes        0.0.0.0:8080->80/tcp   my-running-app
```

The output displays the container ID, image name, status, and port mappings. Look for `my-running-app` to identify your container.

### Stop and Remove the Docker Container

When you’re done using the container, it’s best to stop and remove it to free up system resources. Use the following commands:

```markdown
    ```bash {name=docker-stop-apache,tag=docker-example}
    CONTAINER_ID=$(docker ps -aqf "name=my-running-app")
    docker stop $CONTAINER_ID && docker rm $CONTAINER_ID
    ```
```

#### Explanation:
- **`docker ps -aqf "name=my-running-app"`**: Finds the container ID of `my-running-app`.
- **`docker stop $CONTAINER_ID`**: Stops the container.
- **`docker rm $CONTAINER_ID`**: Removes the stopped container.

---

## Full Markdown File

The following is the complete Markdown file (`interact-with-docker.md`) that defines all runnable commands discussed above. You can use it with `RunMD` to execute each step interactively:

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

        When you're done, it’s a good practice to stop and remove the container to free up resources. The following command stops and removes the container named `my-running-app`.

        ```bash {name=docker-stop-apache,tag=docker-example}
        CONTAINER_ID=$(docker ps -aqf "name=my-running-app")
        docker stop $CONTAINER_ID && docker rm $CONTAINER_ID
        ```