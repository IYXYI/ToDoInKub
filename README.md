# kube-todo

A full-stack Kubernetes project with a Flask backend, React frontend, PostgreSQL, and a monitoring stack (Prometheus, Grafana, Alertmanager).

## Features
- **Backend:** Flask API with CRUD for todos, metrics endpoint for Prometheus
- **Frontend:** React app calling backend API
- **Database:** PostgreSQL (StatefulSet)
- **Kubernetes:** Deployments, Services, Ingress, Monitoring
- **CI/CD:** GitHub Actions workflow for Docker build/push and deployment
- **Monitoring:** Prometheus scrapes backend and cluster, Grafana dashboards, Alertmanager alerts on backend pod restarts

## Project Structure
```
backend/           # Flask API + Dockerfile
frontend/          # React app + Dockerfile
k8s/               # Kubernetes manifests
  monitoring/      # Prometheus, Grafana, Alertmanager configs
.github/workflows/ # GitHub Actions workflow
```

## Setup
1. **Build and push images:**
   - On push to `main`, GitHub Actions builds and pushes images to ghcr.io
2. **Kubernetes deployment:**
   - Workflow runs `kubectl apply -f k8s/` (requires KUBECONFIG secret)
3. **Access app:**
   - Ingress exposes `/api` to backend, `/` to frontend (host: `kube-todo.local`)
4. **Monitoring:**
   - Prometheus, Grafana, and Alertmanager run in cluster
   - Grafana default password: `admin`
   - Alert triggers if backend pod restarts >3 times in 10 minutes

## Notes
- Replace Alertmanager Slack webhook in `alertmanager-configmap.yaml`
- For local dev, set up port-forwarding or use a local ingress controller