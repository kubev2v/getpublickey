
[![Operator Repository on Quay](https://quay.io/repository/kubev2v/getpublickey/status "Plugin Repository on Quay")](https://quay.io/repository/kubev2v/getpublickey)

# Welcome to getpublickey - Your Gateway to Cybersecurity Excellence

## Introduction

Welcome to **getpublickey** - the ultimate solution for obtaining the public key of TLS-enabled HTTP servers with unparalleled simplicity and security. In an age where data breaches and cyberattacks are ever-present threats, **getpublickey** empowers you to secure your digital assets by knowing your server's public key.

## What is getpublickey?

**getpublickey** is a Python web service with a RESTful API that allows you to retrieve the public key used by a TLS-enabled HTTP server. It is designed with a security-first approach, using only Python's built-in libraries to minimize attack surfaces, making it resilient against potential vulnerabilities.

## Features

  - **Simplicity:** No external libraries required – just Python's built-in capabilities.
  - **Security:** Minimized attack surfaces for robust protection.
  - **Scalability:** Seamlessly integrate with Docker and Kubernetes for easy deployment.
  - **Reliability:** Rigorously tested on KIND Kubernetes clusters and renowned HTTPS servers.

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

#### To run the getpublickey server:

```bash
python ./src/getpublickey.py
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

  --tls-key and --tls-cert: Point to files containing the server PEM certs. (Default are key.pem and cert.pem)

```bash
python ./src/getpublickey.py --tls-key /path/to/yourkey.pem --tls-cert /path/to/yourcert.pem
```

#### Generate Local Self-Signed Certificates for Testing:

```bash
openssl req -x509 -newkey rsa:4096 -keyout tls.key -out tls.crt -days 365 -nodes
```

### Access the API

With the server up and running, you can access the API to retrieve public keys. Use the `curl` CLI utility:

```bash
curl -k -G https://127.0.0.1:8443/ --data 'url=example.com:443/boards'
```

  Replace the `url` parameter value with the desired server's URL from which you want to retrieve the public key.


### Run Using Container

#### Generating Self-Signed Certificates for Testing

Before running the container, if you need self-signed certificates for testing, you can generate them using the following commands:

```bash
mkdir certs
openssl req -x509 -newkey rsa:4096 -keyout certs/tls.key -out certs/tls.crt -days 365 -nodes
```

This will create a certs directory with two files: `tls.key` (the private key) and `tls.crt` (the certificate).

#### Building the Container Image with Podman

To build the container image using Podman:

```bash
podman build -t quay.io/kubev2v/getpublickey:latest .
```

This command builds the container and tags it as `quay.io/kubev2v/getpublickey:latest`.

#### Running the Container Locally

Once the image is built, you can run it locally using the following command:

```bash
podman run -it -p 8443:443 -v $(pwd)/certs:/var/run/secrets/getpublickey-serving-cert:Z quay.io/kubev2v/getpublickey:latest
```

This command:

  - Maps port 8443 on the host to port 443 in the container.
  - Mounts the `certs` directory (with the self-signed certificates) to `/var/run/secrets/getpublickey-serving-cert` in the container.
  - Uses the `:Z` option to ensure the mounted directory has the correct SELinux label.
  - Runs the container image `quay.io/kubev2v/getpublickey:latest`.

After executing the command, your service should be accessible at `https://localhost:8443`.

## Deployment
Deploying **getpublickey** is a breeze thanks to our meticulously crafted Dockerfile and Kubernetes deployment configuration. You can effortlessly integrate it into your existing infrastructure. Learn more in the Deployment Guide.

## Testing
We take security seriously. **getpublickey** has undergone extensive testing to ensure its reliability and robustness. Find out how to test it on your KIND Kubernetes cluster and renowned HTTPS servers in the Testing Guide.

## Contributing
We welcome contributions from the cybersecurity community! Whether you're interested in adding features, fixing bugs, or improving documentation, your contributions are valuable. See our Contribution Guidelines for details.

## License
**getpublickey** is licensed under the Apache License, making it open and accessible for all. Feel free to use, modify, and share this powerful cybersecurity tool.
