# Deployment Guide for getpublickey Server in Kubernetes

When interacting with a Kubernetes cluster within the `konveyor-forklift` namespace:

> [!NOTE]
> Note for **OpenShift** Users: When using **OpenShift**, the deployment automatically relies on **OpenShift**'s native certification. Therefore, manual deployment of the issuer and certificate, as described for vanilla Kubernetes, might not be necessary, skip the certification sections and go to [Deploying the Server](#deploying-the-server).


## Setting up the Issuer (Cert-Manager) for Vanilla Kubernetes:

On a vanilla Kubernetes cluster, we utilize [cert-manager](https://cert-manager.io/docs/installation/kubernetes/) to manage certificates. If you haven't already, you'll first need to [install cert-manager](https://cert-manager.io/docs/installation/kubernetes/). Once installed, you can proceed to deploy the self-signed issuer:

```bash
# If not installed, install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml
```

Once cert manage is installed, you can apply the issuer

```bash
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/issuer.yaml
```

This action will establish an issuer named forklift-issuer. To verify its presence in your cluster, run:

```arduino
kubectl get issuer -n konveyor-forklift
```

## Generating Certificates:

Next, apply the certificate configuration to generate a secret named getpublickey-serving-cert:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/certificate.yaml
```

## Deploying the Server:

Finally, deploy the getpublickey server pod and its associated service, which will utilize the getpublickey-serving-cert secret:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/deployment.yaml
```

> [!NOTE]
> Testin the service deployment locally:
>
> Port forwart the service to the local machine:
> ```bash
> kubectl port-forward svc/getpublickey 8443:8443 -n konveyor-forklift
> ```
>
> Fetch a public key from a URL available inside the cluster:
> ```bash
> curl -k -G https://127.0.0.1:8443/ --data 'url=github.com'
> ```
