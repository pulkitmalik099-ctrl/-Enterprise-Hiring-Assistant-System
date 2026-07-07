# Phase 4: Deployment Guide - Complete

## Overview

Phase 4 provides comprehensive infrastructure for deploying the Enterprise Hiring Assistant System to production environments using Kubernetes, with monitoring, security, and auto-scaling capabilities.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture](#architecture)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Monitoring & Logging](#monitoring--logging)
6. [Security](#security)
7. [Auto-Scaling](#auto-scaling)
8. [Backup & Disaster Recovery](#backup--disaster-recovery)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

- **kubectl** v1.24+
  ```bash
  curl -LO "https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl"
  chmod +x kubectl && sudo mv kubectl /usr/local/bin/
  ```

- **Kustomize** v4.0+
  ```bash
  curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
  sudo mv kustomize /usr/local/bin/
  ```

- **Helm** 3.0+ (optional, for package management)
  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```

- **Docker** for building images
- **Azure CLI** or **AWS CLI** for cloud deployment

### Cloud Accounts

- **Azure**: AKS (Azure Kubernetes Service) cluster
- **AWS**: EKS (Elastic Kubernetes Service) cluster
- **GCP**: GKE (Google Kubernetes Engine) cluster

### Required Secrets

Store these in GitHub Secrets or your CI/CD platform:

```yaml
# Azure
AZURE_SUBSCRIPTION_ID: xxxx
AZURE_TENANT_ID: xxxx
AZURE_CLIENT_ID: xxxx
AZURE_CLIENT_SECRET: xxxx

# AWS
AWS_ACCESS_KEY_ID: xxxx
AWS_SECRET_ACCESS_KEY: xxxx

# API Keys
ANTHROPIC_API_KEY: sk-ant-xxxx
OPENAI_API_KEY: sk-xxxx

# Slack (notifications)
SLACK_WEBHOOK: https://hooks.slack.com/...
```

## Architecture

### Kubernetes Components

```
┌─────────────────────────────────────────────────┐
│           Kubernetes Cluster (AKS/EKS)          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Ingress/nginx   │  │   cert-manager   │   │
│  │  (SSL/TLS)       │  │   (Let's Encrypt)│   │
│  └────────┬─────────┘  └──────────────────┘   │
│           │                                     │
│  ┌────────▼────────┐  ┌──────────────────┐   │
│  │  Frontend (2-3) │  │  Backend (3-5)   │   │
│  │  Replicas       │  │  Replicas        │   │
│  │  HPA Enabled    │  │  HPA Enabled     │   │
│  └─────────────────┘  └────────┬─────────┘   │
│                                 │              │
│  ┌─────────────────────┬────────▼───────┐    │
│  │    PostgreSQL       │     Redis      │    │
│  │    StatefulSet      │   Cache Layer  │    │
│  │                     │                │    │
│  └─────────────────────┴────────────────┘    │
│                                               │
│  ┌─────────────────────┬────────────────┐   │
│  │  Prometheus         │   Grafana      │   │
│  │  Monitoring         │   Dashboard    │   │
│  └─────────────────────┴────────────────┘   │
│                                               │
└─────────────────────────────────────────────────┘
```

## Kubernetes Deployment

### Directory Structure

```
k8s/
├── base/                          # Base configurations
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── hpa.yaml
│   ├── network-policies.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/                       # Development overlay
    │   ├── kustomization.yaml
    │   └── deployment-patch.yaml
    ├── staging/                   # Staging overlay
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   ├── monitoring.yaml
    │   ├── rbac.yaml
    │   └── backup-policy.yaml
    └── prod/                      # Production overlay
        ├── kustomization.yaml
        ├── deployment-patch.yaml
        ├── monitoring.yaml
        ├── rbac.yaml
        ├── backup-policy.yaml
        └── secrets.env
```

### Deployment Steps

#### 1. Create Kubernetes Namespace

```bash
kubectl create namespace hiring
kubectl label namespace hiring name=hiring
```

#### 2. Create Secrets

```bash
kubectl create secret generic hiring-secrets \
  --from-literal=database-url='postgresql://user:pass@postgres:5432/db' \
  --from-literal=anthropic-api-key='sk-ant-xxxx' \
  --from-literal=secret-key='your-secret-key' \
  -n hiring

kubectl create secret generic postgresql-secret \
  --from-literal=username='hiring_user' \
  --from-literal=password='secure_password' \
  -n hiring
```

#### 3. Apply Kustomize Configuration

```bash
# Development
kustomize build k8s/overlays/dev | kubectl apply -f -

# Staging
kustomize build k8s/overlays/staging | kubectl apply -f -

# Production
kustomize build k8s/overlays/prod | kubectl apply -f -
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n hiring

# Check services
kubectl get svc -n hiring

# Check ingress
kubectl get ingress -n hiring

# View logs
kubectl logs -f deployment/hiring-backend -n hiring
kubectl logs -f deployment/hiring-frontend -n hiring
```

### Update Deployment

```bash
# Update image and trigger rollout
kustomize edit set image \
  ghcr.io/pulkitmalik099-ctrl/enterprise-hiring-assistant=ghcr.io/pulkitmalik099-ctrl/enterprise-hiring-assistant:v1.0.1 \
  -k k8s/overlays/prod

kustomize build k8s/overlays/prod | kubectl apply -f -

# Wait for rollout
kubectl rollout status deployment/hiring-backend -n hiring
```

## Cloud Deployment

### Azure AKS

#### 1. Create AKS Cluster

```bash
# Create resource group
az group create \
  --name hiring-assistant-rg \
  --location eastus

# Create AKS cluster
az aks create \
  --resource-group hiring-assistant-rg \
  --name hiring-aks-prod \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets \
  --enable-managed-identity \
  --network-plugin azure \
  --enable-addons monitoring \
  --zones 1 2 3
```

#### 2. Configure kubectl

```bash
az aks get-credentials \
  --resource-group hiring-assistant-rg \
  --name hiring-aks-prod
```

#### 3. Install Ingress Controller

```bash
# Add Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install nginx ingress
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

#### 4. Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

### AWS EKS

#### 1. Create EKS Cluster

```bash
# Using eksctl (recommended)
eksctl create cluster \
  --name hiring-eks-prod \
  --version 1.28 \
  --region us-east-1 \
  --nodegroup-name standard-nodes \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10
```

#### 2. Configure kubectl

```bash
aws eks update-kubeconfig \
  --name hiring-eks-prod \
  --region us-east-1
```

#### 3. Install AWS Load Balancer Controller

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=hiring-eks-prod
```

### GCP GKE

#### 1. Create GKE Cluster

```bash
gcloud container clusters create hiring-gke-prod \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10 \
  --enable-ip-alias
```

#### 2. Configure kubectl

```bash
gcloud container clusters get-credentials hiring-gke-prod \
  --zone us-central1-a
```

## Monitoring & Logging

### Prometheus Setup

```yaml
# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Key Metrics to Monitor

```
Backend:
- http_requests_total          # Total requests
- http_request_duration        # Request latency
- database_query_duration      # DB performance
- cache_hit_ratio              # Cache effectiveness
- ai_agent_processing_time     # Agent performance
- error_rate                   # Error percentage

Frontend:
- page_load_time               # User experience
- javascript_errors            # JS errors
- api_call_latency             # API performance

Infrastructure:
- pod_cpu_usage                # CPU utilization
- pod_memory_usage             # Memory utilization
- pod_restart_count            # Stability
- disk_usage                   # Storage
- network_io                   # Network traffic
```

### Alerting Rules

Key alerts configured in `k8s/overlays/prod/monitoring.yaml`:

- High error rate (> 5% errors)
- High memory usage (> 90%)
- High CPU usage (> 80%)
- Database down (pg_up = 0)
- API latency high (p95 > 1s)

### Logging Stack

```bash
# Install ELK Stack
helm repo add elastic https://helm.elastic.co
helm repo update

# Elasticsearch
helm install elasticsearch elastic/elasticsearch \
  --namespace logging \
  --create-namespace

# Kibana
helm install kibana elastic/kibana \
  --namespace logging

# Filebeat
helm install filebeat elastic/filebeat \
  --namespace logging
```

### Accessing Dashboards

```bash
# Port forward to Prometheus
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Port forward to Kibana
kubectl port-forward -n logging svc/kibana 5601:5601
```

## Security

### Network Policies

Network policies restrict traffic between pods:

```yaml
# Backend can only accept from Frontend and Ingress
# Frontend can only accept from Ingress
# Database and Redis only accept from Backend
# All outbound HTTPS allowed for API calls
```

### Pod Security Policies

```yaml
# Non-root user (UID 1000)
# Read-only root filesystem
# No privilege escalation
# Dropped capabilities (ALL)
# Resource limits enforced
```

### Secret Management

### Option 1: Sealed Secrets

```bash
# Install sealed-secrets
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# Seal a secret
echo -n 'mypassword' | kubectl create secret generic mysecret \
  --dry-run=client \
  --from-file=/dev/stdin \
  | kubeseal -f - > mysealedsecret.yaml

# Apply sealed secret
kubectl apply -f mysealedsecret.yaml
```

### Option 2: External Secrets Operator

```bash
# Install external-secrets
helm repo add external-secrets https://external-secrets.github.io/charts
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace
```

### TLS/SSL Configuration

- **Ingress TLS**: Let's Encrypt certificates via cert-manager
- **Database Connection**: SSL/TLS enabled
- **API Communication**: HTTPS enforced
- **Certificate Renewal**: Automatic via cert-manager

### RBAC (Role-Based Access Control)

```yaml
# ServiceAccounts: hiring-backend, hiring-frontend
# Roles: Minimal permissions required
# RoleBindings: Connect roles to service accounts
# ClusterRoles: For cluster-wide resources
```

## Auto-Scaling

### Horizontal Pod Autoscaler (HPA)

#### Backend Scaling

```yaml
Min Replicas: 3
Max Replicas: 10
CPU Target: 70%
Memory Target: 80%

Scale Up:
- +100% pods per 15s if high load
- +2 pods per 15s if high load

Scale Down:
- -50% pods every 5min if low load
```

#### Frontend Scaling

```yaml
Min Replicas: 2
Max Replicas: 8
CPU Target: 75%
Memory Target: 85%
```

### Vertical Pod Autoscaler (Optional)

```bash
# Install VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

## Backup & Disaster Recovery

### Database Backups

**Automated daily backups at 2 AM UTC:**

```bash
# Backup includes:
- Full PostgreSQL database dump
- Compressed (gzip)
- Uploaded to S3 (if configured)
- Retention: 30 days

# Restore from backup
gunzip db_backup_20240101_020000.sql.gz
psql -h localhost -U hiring_user hiring_db < db_backup_20240101_020000.sql
```

### Disaster Recovery Plan

#### RPO (Recovery Point Objective)
- **Data**: 24 hours (daily backups)
- **Configuration**: 15 minutes (GitOps)
- **Secrets**: Encrypted and backed up

#### RTO (Recovery Time Objective)
- **Application**: < 5 minutes (Kubernetes redeploy)
- **Database**: < 30 minutes (restore from backup)
- **Full System**: < 1 hour

#### Recovery Steps

```bash
# 1. Restore from backup
gunzip backup.sql.gz
psql -f backup.sql

# 2. Reapply Kustomize config
kustomize build k8s/overlays/prod | kubectl apply -f -

# 3. Verify pods are running
kubectl get pods -n hiring

# 4. Test health endpoints
curl https://hiring-assistant.example.com/health
```

## Production Checklist

- [ ] Kubernetes cluster created and configured
- [ ] Namespaces created (dev, staging, prod)
- [ ] Secrets and ConfigMaps applied
- [ ] Ingress controller installed
- [ ] cert-manager installed and configured
- [ ] Prometheus/Grafana installed
- [ ] ELK stack installed
- [ ] Network policies applied
- [ ] Resource quotas set
- [ ] HPA configured
- [ ] Backup jobs scheduled
- [ ] RBAC configured
- [ ] DNS configured (hiring-assistant.example.com)
- [ ] SSL certificates installed
- [ ] Monitoring alerts configured
- [ ] Logging aggregation working
- [ ] Disaster recovery tested
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation complete

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n hiring

# View logs
kubectl logs <pod-name> -n hiring

# Check events
kubectl get events -n hiring --sort-by='.lastTimestamp'
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgres -U hiring_user -d hiring_db -c "SELECT 1"
```

### Memory/CPU Issues

```bash
# Check resource usage
kubectl top pods -n hiring
kubectl top nodes

# Check resource limits
kubectl describe nodes
```

### Ingress Not Working

```bash
# Check ingress status
kubectl get ingress -n hiring
kubectl describe ingress hiring-ingress -n hiring

# Check ingress controller
kubectl get pods -n ingress-nginx
kubectl logs -f deployment/nginx-ingress-controller -n ingress-nginx
```

## Maintenance

### Regular Tasks

- **Weekly**: Review monitoring dashboards
- **Weekly**: Check backup status
- **Monthly**: Review logs and errors
- **Monthly**: Update security patches
- **Quarterly**: Disaster recovery drill
- **Quarterly**: Capacity planning review

### Scaling Resources

```bash
# Increase cluster nodes
az aks nodepool scale \
  --resource-group hiring-assistant-rg \
  --cluster-name hiring-aks-prod \
  --name nodepool1 \
  --node-count 5
```

### Updating Applications

```bash
# Blue-green deployment
kubectl set image deployment/hiring-backend \
  backend=ghcr.io/pulkitmalik099-ctrl/enterprise-hiring-assistant:v1.1.0 \
  -n hiring

# Verify rollout
kubectl rollout status deployment/hiring-backend -n hiring
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Azure AKS](https://docs.microsoft.com/en-us/azure/aks/)
- [AWS EKS](https://docs.aws.amazon.com/eks/)
- [GCP GKE](https://cloud.google.com/kubernetes-engine/docs)
- [Kustomize](https://kustomize.io/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Cert-Manager](https://cert-manager.io/)
- [sealed-secrets](https://github.com/bitnami-labs/sealed-secrets)

---

**Status**: ✅ Phase 4 Complete
**Last Updated**: 2026-07-08
**Production Ready**: Yes
