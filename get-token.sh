#!/bin/sh
#
# ScaleIO FlexVolume utility for obtaining token 
#
# Do not modify thist script, configuration settings can be found at
# /opt/emc/scaleio/flexvolume/cfg/config

# Set SERVICE_ACC to desired/existing service account; KUBECONFIG needs to have permissions to get secret/ticket from SERVICE_ACC 
SERVICE_ACC=scaleio-flex-volume

CONFIGFILE="/opt/emc/scaleio/flexvolume/cfg/config"
if [ -x "${CONFIGFILE}" ]; then
  # source the config file
        source "${CONFIGFILE}"
fi

# in case some values were not specific in the config file, set their values
KUBECONFIG="${KUBECONFIG:-/root/.kube/config}"

WHICH_OC=$(which oc > /dev/null 2>&1)
WHICH_OC_RETURN=$(echo $?)
if [ "${WHICH_OC_RETURN}" = "0" ]; then
	CMD="oc"
	CONFIG_OPTION="--config"
else
	CMD="kubectl"
	CONFIG_OPTION="--kubeconfig"
fi

secret=$(${CMD} ${CONFIG_OPTION}=${KUBECONFIG} get sa ${SERVICE_ACC} --template='{{range .secrets}}{{.name}}{{"\n"}}{{end}}' | grep token)
token=$(${CMD} ${CONFIG_OPTION}=${KUBECONFIG} get secret ${secret} --template='{{ .data.token}}' | base64 -d)

echo -n ${token}
