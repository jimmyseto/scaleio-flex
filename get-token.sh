#!/bin/bash

secret=$(oc --config=/path/to/kubeconfig get sa scaleio-flex-volume --template='{{range .secrets}}{{.name}}{{"\n"}}{{end}}' | grep token)
token=$(oc --config=/path/to/kubeconfig get secret $secret --template='{{ .data.token}}' | base64 -d)

echo -n $token
