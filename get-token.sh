#!/bin/sh

# Set KUBECONFIG to point to desired config file; ensure specified config file exists on all nodes 
KUBECONFIG=/root/.kube/config

# Set SERVICE_ACC to desired/existing service account; KUBECONFIG needs to have permissions to get secret/ticket from SERVICE_ACC 
SERVICE_ACC=scaleio-flex-volume

secret=$(oc --config=${KUBECONFIG} get sa ${SERVICE_ACC} --template='{{range .secrets}}{{.name}}{{"\n"}}{{end}}' | grep token)
token=$(oc --config=${KUBECONFIG} get secret ${secret} --template='{{ .data.token}}' | base64 -d)

echo -n ${token}
