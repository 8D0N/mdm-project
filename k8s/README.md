Purpose
- Manifests and instructions to deploy the Windows MDM app to Oracle Kubernetes (OKE).

Quick start (build & push image to OCIR)
1. Build image locally (replace with your OCIR namespace):
```bash
docker build -f docker/prod.Dockerfile -t <region-key>.ocir.io/<tenancy-namespace>/mdm-server:latest .
docker push <region-key>.ocir.io/<tenancy-namespace>/mdm-server:latest
```

2. Update `k8s/deployment.yaml` image to the pushed image reference.

Apply manifests (after creating any needed namespaces):
```bash
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
```

Notes
- For production, use OCI Vault or Kubernetes Secrets with proper RBAC and avoid storing plaintext credentials in repo.
- Consider using HorizontalPodAutoscaler and readiness/liveness probes.
