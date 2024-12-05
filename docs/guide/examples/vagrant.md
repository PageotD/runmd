# Interact with Vagrant

This guide walks you through setting up, running, and managing a basic Vagrant environment. By following these steps, you’ll learn how to:

- Create a `Vagrantfile` to define your environment.
- Initialize and start a virtual machine (VM).
- SSH into the VM and provision it with software.
- Manage and clean up Vagrant environments.

---

## Step 1: Create a `Vagrantfile`

A `Vagrantfile` is a configuration file that defines your virtual machine (VM) environment. Create a file named `Vagrantfile` with the following content:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
end
```

### Explanation:

- **`Vagrant.configure("2")`**: Specifies the configuration version (always use `2` for modern Vagrant setups).
- **`config.vm.box`**: Specifies the base box image to use. In this example, it’s `hashicorp/bionic64` (Ubuntu 18.04).
- **`config.vm.network`**: Sets up a port forwarding rule to map port `80` in the VM to port `8080` on your host machine.

---

## Step 2: Initialize and Start the Vagrant VM

With your `Vagrantfile` ready, initialize the environment and start the VM.

### Initialize the Environment

Run the following command to initialize the Vagrant environment (if it hasn’t been done already):

```markdown
    ```bash {name=vagrant-init,tag=vagrant-example}
    vagrant init hashicorp/bionic64
    ```
```

This downloads the base box (`hashicorp/bionic64`) and prepares your environment.

### Start the VM

Start the VM with:

```markdown
    ```bash {name=vagrant-up,tag=vagrant-example}
    vagrant up
    ```
```

This creates and starts the VM, downloading the base image if necessary.

---

## Step 3: Interact with the VM

After the VM is running, you can interact with it.

### SSH into the VM

To log into the VM via SSH, use:

```markdown
    ```bash {name=vagrant-ssh,tag=vagrant-example}
    vagrant ssh
    ```
```

This gives you shell access to the VM. You can now install software, modify configurations, and more.

---

## Step 4: Manage and Clean Up the Environment

### Suspend the VM

If you want to pause the VM (save its state), use:

```markdown
    ```bash {name=vagrant-suspend,tag=vagrant-example}
    vagrant suspend
    ```
```

### Destroy the VM

To stop and remove the VM entirely, run:

```markdown
    ```bash {name=vagrant-destroy,tag=vagrant-example}
    vagrant destroy -f
    ```
```

---

## Full Markdown File

Here’s the complete Markdown file (`interact-with-vagrant.md`) that defines all runnable commands discussed above. You can use it with `RunMD` to execute each step interactively:

!!! example "interact-with-vagrant.md"

    ```markdown
        # Interact with Vagrant

        ## Initialize and Start the Vagrant VM

        Run the following commands to initialize and start the VM using the `hashicorp/bionic64` box.

        ```bash {name=vagrant-init,tag=vagrant-example}
        vagrant init hashicorp/bionic64
        ```

        ```bash {name=vagrant-up,tag=vagrant-example}
        vagrant up
        ```

        ## SSH into the VM

        Once the VM is running, log in via SSH with:

        ```bash {name=vagrant-ssh,tag=vagrant-example}
        vagrant ssh
        ```

        ## Suspend and Destroy the VM

        To suspend the VM (save its state), use:

        ```bash {name=vagrant-suspend,tag=vagrant-example}
        vagrant suspend
        ```

        To completely remove the VM, use:

        ```bash {name=vagrant-destroy,tag=vagrant-example}
        vagrant destroy -f
        ```
    ```