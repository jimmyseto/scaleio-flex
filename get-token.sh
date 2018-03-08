#!/bin/bash

secret=$(oc get sa scaleio-flex-volume --template='{{range .secrets}}{{.name}}{{"\n"}}{{end}}' | grep token)
token=$(oc get secret $secret --template='{{ .data.token}}' | base64 -d)

echo -n $token
