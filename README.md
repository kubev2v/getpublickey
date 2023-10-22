

<p align="center">
  <img src="./getpublickey.svg" alt="getpublickey Logo">
</p>

[![Operator Repository on Quay](https://quay.io/repository/kubev2v/getpublickey/status "Plugin Repository on Quay")](https://quay.io/repository/kubev2v/getpublickey)

# getpublickey

Monitor public keys for services running on a disconnected private network.

## Table of content:

  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
    - [Clone the Repository](#clone-the-repository)
    - [Configure Your Environment](#configure-your-environment)
    - [Run the Server](#run-the-server)
    - [Access the API](#access-the-api)
    - [Run Using Container](#run-using-container)

## Introduction

**getpublickey** is a utility that provides an API for applications to obtain the public key of a service. This is particularly valuable in secure environments where services utilize self-signed keys. Instead of disabling certificate verification within the secure network, this utility enables them to utilize TLS by retrieving the self-signed public key, allowing users to verify the acquired public key before using it for further communication.

> [!NOTE]  
>  This utility is intended for applications that can't fetch the publick key directly, for example applications that run on a network that does not have access to the service. If your applicaion have access to the service you can get a public key without the need of a service running on a different network.
>
> For example if the service is running on the same network you can use command line tools like `openssl` to get the public key directly:
>
> `echo | openssl s_client -connect google.com:443 2>/dev/null | openssl x509 -text`


## Getting Started

To start using **getpublickey**, follow these simple steps:

### Clone the Repository

To get started with getpublickey, the first step is to clone the repository to your local machine.

```bash
git clone https://github.com/kubev2v/getpublickey.git
cd getpublickey
```

### Configure Your Environment

Before you run the server, ensure your environment is properly set up:

Install Python: getpublickey requires Python to run. If you haven't already, [download and install Python](https://www.python.org/downloads/).

#### Optional Libraries for Linting:

Install `isort` for imports sorting:

```bash
pip install isort
```

Install `black` for code formatting:

```bash
pip install black
```

#### Optional Tools for Containerization:

Install `podman` if you wish to build and use container images. [Follow the installation guide](https://podman.io/getting-started/installation) specific to your operating system.

#### Optional Tools for Cluster Deployment:

Set up a `kind` Kubernetes cluster if you want to run the server in a cluster environment. Detailed instructions can be [found on the kind GitHub repository](https://github.com/kubernetes-sigs/kind).

### Run the Server

#### To run the getpublickey locally:

```bash
python ./src/getpublickey.py --help
```

#### Optional Flags:

  --port: Specify the port for the server to listen to. (Default is 8443)

```bash
python ./src/getpublickey.py --port 8080
```

  --listen: Set the listen address. (Default is 0.0.0.0)

```bash
python ./src/getpublickey.py --listen 192.168.1.100
```

  --tls-key and --tls-cert: Point to files containing the server PEM certs. (Default are tls.key and tls.crt)

```bash
python ./src/getpublickey.py --tls-key certs/tls.key --tls-cert certs/tls.crt
```

#### Generate Local Self-Signed Certificates for Testing:

```bash
mkdir certs
openssl req -x509 -newkey rsa:4096 -keyout certs/tls.key -out certs/tls.crt -days 365 -nodes
```

> [!NOTE]  
> This will create a certs directory with two files: `tls.key` (the private key) and `tls.crt` (the certificate).

### Access the API

With the server up and running, you can access the API to retrieve public keys. Use the `curl` CLI utility:

```bash
curl -k -G https://127.0.0.1:8443/ --data 'url=github.com'
```

> [!NOTE] 
> Replace the `url` parameter value with the desired server's URL from which you want to retrieve the public key.


### Run Using Container

#### Building the Container Image with Podman

To build the container image using Podman:

```bash
podman build -t quay.io/kubev2v/getpublickey:latest .
```

This command builds the container and tags it as `quay.io/kubev2v/getpublickey:latest`.

#### Running the Container Locally

Once the image is built, you can run it locally using the following command:

```bash
podman run -it -p 8443:8443 \
  -v $(pwd)/certs:/var/run/secrets/getpublickey-serving-cert:Z \
  quay.io/kubev2v/getpublickey:latest
```

> [!NOTE] 
> This command:
>
>  - Maps port 8443 on the host to port 8443 in the container.
>  - Mounts the `certs` directory (with the self-signed certificates) to `/var/run/secrets/getpublickey-serving-cert` in the container.
>  - Uses the `:Z` option to ensure the mounted directory has the correct SELinux label.
>  - Runs the container image `quay.io/kubev2v/getpublickey:latest`.

After executing the command, your service should be accessible at `https://localhost:8443`.

### Setting up the 'getpublickey' Server on a Kubernetes Cluster

Follow these guidelines to deploy the getpublickey server on a Kubernetes cluster:

#### Preparation Steps

  - Make sure you've installed kubectl and have set it up correctly to interact with your cluster.
Ensure you possess the rights to initiate new namespaces and deployments within the cluster.

  - Ensure you have `kubectl` installed and properly configured to communicate with your cluster.
You need permissions to create new `namespaces` and `deployments` on the cluster.

#### Launching the Service on an External Kubernetes Cluster

  - Cluster Authentication: Confirm that you're connected to your Kubernetes cluster and have the requisite privileges.
  - Application Deployment: Refer to the ['ci' folder](./ci) for detailed instructions on deploying the getpublickey service to an external cluster.
