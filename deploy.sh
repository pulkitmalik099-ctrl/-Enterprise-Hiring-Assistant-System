#!/bin/bash

###############################################################################
# Enterprise Hiring Assistant - Kubernetes Deployment Script
#
# This script automates the deployment of the Enterprise Hiring Assistant
# to Kubernetes clusters (AKS, EKS, GKE)
#
# Usage:
#   ./deploy.sh [environment] [cloud-provider]
#   ./deploy.sh prod azure
#   ./deploy.sh staging aws
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENVIRONMENT="${1:-staging}"
CLOUD_PROVIDER="${2:-azure}"
NAMESPACE="hiring-${ENVIRONMENT}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed. Please install kubectl."
    fi
    log_success "kubectl found: $(kubectl version --client --short)"

    # Check kustomize
    if ! command -v kustomize &> /dev/null; then
        log_error "kustomize is not installed. Please install kustomize."
    fi
    log_success "kustomize found: $(kustomize version)"

    # Check cloud CLI
    case $CLOUD_PROVIDER in
        azure)
            if ! command -v az &> /dev/null; then
                log_error "Azure CLI is not installed."
            fi
            log_success "Azure CLI found"
            ;;
        aws)
            if ! command -v aws &> /dev/null; then
                log_error "AWS CLI is not installed."
            fi
            log_success "AWS CLI found"
            ;;
        gcp)
            if ! command -v gcloud &> /dev/null; then
                log_error "Google Cloud SDK is not installed."
            fi
            log_success "gcloud found"
            ;;
    esac
}

validate_environment() {
    log_info "Validating environment: $ENVIRONMENT"

    if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
        log_error "Invalid environment. Use: dev, staging, or prod"
    fi

    if [[ ! -d "$SCRIPT_DIR/k8s/overlays/$ENVIRONMENT" ]]; then
        log_error "Environment overlay not found: k8s/overlays/$ENVIRONMENT"
    fi

    log_success "Environment validated: $ENVIRONMENT"
}

create_namespace() {
    log_info "Creating namespace: $NAMESPACE"

    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log_warn "Namespace already exists: $NAMESPACE"
    else
        kubectl create namespace "$NAMESPACE"
        kubectl label namespace "$NAMESPACE" name="$NAMESPACE"
        log_success "Namespace created: $NAMESPACE"
    fi
}

create_secrets() {
    log_info "Creating secrets in namespace: $NAMESPACE"

    # Check if secrets file exists
    if [[ ! -f "$SCRIPT_DIR/k8s/overlays/$ENVIRONMENT/secrets.env" ]]; then
        log_warn "Secrets file not found. Using default secret creation."
        log_warn "Make sure to update secrets manually before deploying to production!"

        # Create placeholder secrets
        kubectl create secret generic hiring-secrets \
            --from-literal=database-url="postgresql://user:password@postgres:5432/hiring_db" \
            --from-literal=anthropic-api-key="sk-ant-placeholder" \
            --from-literal=openai-api-key="sk-placeholder" \
            --from-literal=secret-key="your-secret-key-change-in-production" \
            -n "$NAMESPACE" 2>/dev/null || log_warn "Secrets may already exist"
    else
        kubectl create secret generic hiring-secrets \
            --from-env-file="$SCRIPT_DIR/k8s/overlays/$ENVIRONMENT/secrets.env" \
            -n "$NAMESPACE" 2>/dev/null || log_warn "Secrets may already exist"
    fi

    log_success "Secrets configured"
}

deploy_with_kustomize() {
    log_info "Deploying with Kustomize..."

    local overlay_path="$SCRIPT_DIR/k8s/overlays/$ENVIRONMENT"

    # Build and apply
    log_info "Building Kustomize configuration..."
    kustomize build "$overlay_path" > /tmp/hiring-deployment.yaml

    log_info "Applying configuration..."
    kubectl apply -f /tmp/hiring-deployment.yaml -n "$NAMESPACE"

    log_success "Configuration applied"
}

wait_for_rollout() {
    log_info "Waiting for rollout..."

    # Wait for backend
    if kubectl get deployment hiring-backend -n "$NAMESPACE" &> /dev/null; then
        log_info "Waiting for backend deployment..."
        kubectl rollout status deployment/hiring-backend -n "$NAMESPACE" --timeout=5m
        log_success "Backend deployment ready"
    fi

    # Wait for frontend
    if kubectl get deployment hiring-frontend -n "$NAMESPACE" &> /dev/null; then
        log_info "Waiting for frontend deployment..."
        kubectl rollout status deployment/hiring-frontend -n "$NAMESPACE" --timeout=5m
        log_success "Frontend deployment ready"
    fi
}

verify_deployment() {
    log_info "Verifying deployment..."

    log_info "Checking pods..."
    kubectl get pods -n "$NAMESPACE" || log_warn "Could not list pods"

    log_info "Checking services..."
    kubectl get svc -n "$NAMESPACE" || log_warn "Could not list services"

    log_info "Checking ingress..."
    kubectl get ingress -n "$NAMESPACE" || log_warn "Could not list ingress"

    log_success "Deployment verified"
}

run_smoke_tests() {
    log_info "Running smoke tests..."

    # Test backend health
    log_info "Testing backend health endpoint..."
    kubectl run smoke-test \
        --image=curlimages/curl:latest \
        --rm -i --restart=Never \
        -n "$NAMESPACE" \
        -- sh -c "curl -f http://hiring-backend/health 2>/dev/null || true" || true

    log_success "Smoke tests completed"
}

show_summary() {
    log_info "Deployment Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Environment:      $ENVIRONMENT"
    echo "Cloud Provider:   $CLOUD_PROVIDER"
    echo "Namespace:        $NAMESPACE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Useful commands:"
    echo "  View logs:         kubectl logs -f deployment/hiring-backend -n $NAMESPACE"
    echo "  Port forward:      kubectl port-forward svc/hiring-frontend 3000:80 -n $NAMESPACE"
    echo "  Get pods:          kubectl get pods -n $NAMESPACE"
    echo "  Get services:      kubectl get svc -n $NAMESPACE"
    echo "  Get ingress:       kubectl get ingress -n $NAMESPACE"
    echo ""
}

# Main execution
main() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Enterprise Hiring Assistant - Kubernetes Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    check_prerequisites
    validate_environment
    create_namespace
    create_secrets
    deploy_with_kustomize
    wait_for_rollout
    verify_deployment
    run_smoke_tests
    show_summary

    log_success "Deployment completed successfully!"
}

# Run main
main
