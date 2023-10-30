# Deployment Guide for getpublickey Server in Kubernetes

## Deploying the Server on Openshift cluster:

Deploy the getpublickey server pod and its associated service using `openshift-mtv` namespace on **Openshift** cluster:

```bash
# deploy - deploy the service on openshift-mtv namespace
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/deployment.ocp.yaml

# optional - patch console plugin proxy
kubectl patch consoleplugin forklift-console-plugin \
    --patch-file https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/consoleplugin.patch.yaml \
    --type=merge
```

## Deploying the Server on Vanilla Kubernetes:

Deploy `getpublickey` service on a Kubernetes cluster within the `konveyor-forklift` namespace:

### Setting up the Certificate Issuer (Cert-Manager):

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

### Generating Certificates:

Next, apply the certificate configuration to generate a secret named getpublickey-serving-cert:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/certificate.yaml
```

### Deploying the Server:

Finally, deploy the getpublickey server pod and its associated service, which will utilize the getpublickey-serving-cert secret:

```bash
# deploy - deploy the service on konveyor-forklift namespace
kubectl apply -f https://raw.githubusercontent.com/kubev2v/getpublickey/main/ci/deployment.yaml
```

> [!NOTE]
> For testing the service deployment:
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
