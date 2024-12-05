# Deploying NGINX with Kubernetes

In this guide, we’ll deploy an NGINX server on a Kubernetes cluster using `kubectl`. This walkthrough includes installing `kubectl`, creating a namespace, deploying NGINX, and managing resources.

---

## Prerequisites

Ensure you have the following:

1. **Kubernetes cluster**: A running Kubernetes cluster (e.g., Minikube, K3s, or a cloud provider like GKE, EKS, or AKS).
2. **Linux, macOS, or WSL**: A compatible environment to run Kubernetes commands.
3. **`kubectl` installed**: The Kubernetes CLI tool to interact with your cluster.
4. **Cluster access**: Ensure your `kubectl` is configured correctly (verify using `kubectl get nodes`).

---

## Step 1: Install `kubectl`

### For Linux

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
```

### For macOS (using Homebrew)

```bash
brew install kubectl
```

### Verify Installation

Check that `kubectl` is installed by running:

```bash
kubectl version --client
```

---

## Step 2: Create a Namespace

Namespaces isolate Kubernetes resources. Create a namespace called `nginx-example`:

```markdown
    ```bash {name=k8s-create-namespace,tag=k8s-nginx}
    kubectl create namespace nginx-example
    ```
```

---

## Step 3: Deploy NGINX

We’ll create a **Deployment** resource to manage NGINX replicas. 

### Deployment YAML

Save the following YAML configuration in a file named `nginx-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: nginx-example
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23
        ports:
        - containerPort: 80
```

### Apply the Deployment

Apply the configuration to create the deployment:

```markdown
    ```bash {name=k8s-apply-deployment,tag=k8s-nginx}
    kubectl apply -f nginx-deployment.yaml
    ```
```

---

## Step 4: Expose the Deployment (Service)

Expose the NGINX deployment via a **NodePort** service to access it from outside the cluster.

```markdown
    ```bash {name=k8s-expose-service,tag=k8s-nginx}
    kubectl expose deployment nginx-deployment \
      --type=NodePort \
      --name=nginx-service \
      --namespace=nginx-example \
      --port=80
    ```
```

---

## Step 5: Access the Service

Retrieve the exposed port for the `nginx-service`:

```markdown
    ```bash {name=k8s-get-service,tag=k8s-nginx}
    kubectl get service nginx-service -n nginx-example
    ```
```

Look for the `NodePort` field in the output. For example:

```console
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
nginx-service   NodePort   10.96.108.159   <none>        80:31000/TCP   2m
```

You can now access NGINX by navigating to `http://<node-ip>:31000`, replacing `<node-ip>` with your cluster node’s IP.

For Minikube users, get the node IP using:

```bash
minikube ip
```

---

## Step 6: Manage Kubernetes Resources

Kubernetes allows you to manage, inspect, and clean up resources as needed.

### List Pods

To see the running pods:

```markdown
    ```bash {name=k8s-list-pods,tag=k8s-nginx}
    kubectl get pods -n nginx-example
    ```
```

### Scale the Deployment

Increase or decrease replicas (e.g., scale to 5 replicas):

```markdown
    ```bash {name=k8s-scale-deployment,tag=k8s-nginx}
    kubectl scale deployment nginx-deployment --replicas=5 -n nginx-example
    ```
```

### Clean Up Resources

When finished, delete all resources in the namespace:

```markdown
    ```bash {name=k8s-cleanup,tag=k8s-nginx}
    kubectl delete namespace nginx-example
    ```
```

---

## Full Markdown File

!!! example "interact-with-k8s.md"

    ```markdown
        # Deploying NGINX with Kubernetes

        ## Step 1: Create a Namespace

        ```bash {name=k8s-create-namespace,tag=k8s-nginx}
        kubectl create namespace nginx-example
        ```

        ## Step 2: Apply the Deployment

        ```bash {name=k8s-apply-deployment,tag=k8s-nginx}
        kubectl apply -f nginx-deployment.yaml
        ```

        ## Step 3: Expose the Deployment

        ```bash {name=k8s-expose-service,tag=k8s-nginx}
        kubectl expose deployment nginx-deployment \
          --type=NodePort \
          --name=nginx-service \
          --namespace=nginx-example \
          --port=80
        ```

        ## Step 4: Retrieve Service Details

        ```bash {name=k8s-get-service,tag=k8s-nginx}
        kubectl get service nginx-service -n nginx-example
        ```

        ## Step 5: List Pods

        ```bash {name=k8s-list-pods,tag=k8s-nginx}
        kubectl get pods -n nginx-example
        ```

        ## Step 6: Scale the Deployment

        ```bash {name=k8s-scale-deployment,tag=k8s-nginx}
        kubectl scale deployment nginx-deployment --replicas=5 -n nginx-example
        ```

        ## Step 7: Clean Up Resources

        ```bash {name=k8s-cleanup,tag=k8s-nginx}
        kubectl delete namespace nginx-example
        ```
    ```
