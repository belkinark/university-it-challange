# CSV Processor

A web application for uploading CSV files and calculating statistics for a
selected numeric column. Processing runs asynchronously: the API queues each
request, a worker processes it, and the frontend displays the task status and
results.

## Features

- Upload a CSV file and choose the numeric column to analyze.
- Track task status: queued, processing, completed, or failed.
- View the count, minimum, maximum, and mean for completed tasks.
- Store task data in PostgreSQL and use Redis Streams as the task queue.
- Run the services with Docker Compose or deploy them to Kubernetes on Minikube.
- Automatically restart failed containers and pods.

## Architecture

| Component | Purpose |
| --- | --- |
| `frontend` | Static web interface served by Nginx; proxies API requests. |
| `api_service` | FastAPI application for submitting and viewing tasks. Runs database migrations on startup. |
| `worker_service` | FastAPI-based TaskIQ worker that consumes tasks from Redis and processes CSV data. |
| `postgres` | Persistent storage for task data. |
| `redis` | Redis Streams task broker with append-only persistence enabled. |

## Requirements

- Docker Desktop with Docker Compose, for the Compose setup.
- Minikube and `kubectl`, for the Kubernetes setup.

## Run with Docker Compose

From the repository root, create a local environment file and set a PostgreSQL
password:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set `POSTGRES_PASSWORD` to a password of your choice. Then build
and start all services:

```powershell
docker compose up --build -d
```

Open the application at <http://localhost:8080>. The API is available at
<http://localhost:8000>, with interactive documentation at
<http://localhost:8000/docs>.

Useful commands:

```powershell
docker compose ps
docker compose logs -f
docker compose logs -f api_service
docker compose down
```

`docker compose down` keeps the PostgreSQL and Redis named volumes. To remove
those volumes and their data as well, run `docker compose down -v`.

## Run on Minikube

The Kubernetes manifests are in [`k8s/all.yaml`](k8s/all.yaml). They create
Deployments and Services for all five components, PersistentVolumeClaims for
PostgreSQL and Redis, and startup, liveness, and readiness probes.

### 1. Start Minikube and build the images

Run these commands from the repository root. Building with `minikube image build`
makes the images available inside the Minikube cluster:

```powershell
minikube start
minikube image build -t university-api:dev -f api_service/Dockerfile .
minikube image build -t university-worker:dev -f worker_service/Dockerfile .
minikube image build -t university-frontend:dev ./frontend
```

### 2. Create the database password Secret

Choose a password and create the Kubernetes Secret. The password is not stored
in the repository:

```powershell
kubectl create secret generic app-secrets --from-literal=POSTGRES_PASSWORD='your-strong-password'
```

### 3. Deploy the application

```powershell
kubectl apply -f k8s/all.yaml
kubectl get pods -w
```

When all pods are ready, open a **second** PowerShell window and forward the
frontend Service to your computer:

```powershell
kubectl port-forward service/frontend 8080:80
```

Open <http://localhost:8080>.

### 4. Check status and logs

```powershell
kubectl get deployments
kubectl get pods
kubectl logs deployment/api-service
kubectl logs deployment/worker-service
kubectl describe pod <pod-name>
```

The API runs database migrations on startup. If PostgreSQL or Redis is still
starting, the API may restart until its dependencies are available. Kubernetes
will retry automatically; use the commands above to inspect startup failures.

To confirm that a Deployment replaces a deleted pod:

```powershell
kubectl delete pod -l app=worker-service
kubectl get pods -w
```

If a container exits or fails its liveness probe, Kubernetes restarts it. If a
pod is deleted or becomes unrecoverable, its Deployment creates a replacement.
Readiness probes keep unready application pods out of Service traffic.

After changing an image, rebuild it and restart the corresponding Deployment.
For example:

```powershell
minikube image build -t university-api:dev -f api_service/Dockerfile .
kubectl rollout restart deployment/api-service
kubectl rollout status deployment/api-service
```

To remove the Kubernetes resources:

```powershell
kubectl delete -f k8s/all.yaml
```

This also removes the PostgreSQL and Redis PVCs; depending on the cluster's
storage provisioner, their data may be deleted.

## API

The main task endpoints are:

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/v1/tasks/` | Submit a CSV file and the name of its numeric column. |
| `GET` | `/api/v1/tasks/` | List tasks and their status or results. |
| `GET` | `/api/v1/tasks/{task_id}` | Get a task by ID. |

The API's interactive documentation is available at `/docs`.

## Configuration

Docker Compose reads variable overrides from the root `.env` file. Start with
[`.env.example`](.env.example). The services use these settings:

| Variable | Description |
| --- | --- |
| `POSTGRES_HOST`, `POSTGRES_PORT` | PostgreSQL address. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | PostgreSQL database credentials. |
| `POSTGRES_ECHO` | Enable or disable SQLAlchemy SQL logging. |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` | Redis address and database number. |
| `DEBUG` | Application debug setting. |

In Docker Compose and Kubernetes, the database and Redis hosts are set to the
service names `postgres` and `redis`. Do not use `127.0.0.1` for container-to-
container connections.
