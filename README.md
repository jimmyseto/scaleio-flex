Dell ScaleIO FlexVolume Driver
=======

This driver allows users to consume ScaleIO storage, and provide persistent storage to applications running in Kubernetes or OpenShift environments.

## Requirements

* Kubernetes/OpenShift's controller-managed attachment and detachment feature must be enabled.  This feature is enabled by default.  Ensure explicit actions were not taken to disable it.
* For a given ScaleIO volume /dev/disk/by-id/emc-vol-``*``-``<volumeID>``, ``<volumeID>`` must be used throughout as a specifier.  More specifically... 
  * For PersistentVolume:
    * *.metadata.name*
    * *.spec.flexVolume.options.volumeID*
  * For Pod:
    * *.spec.containers.volumeMounts.name*
    * *.spec.volumes.name*
  * For Deployment:
    * *.spec.template.spec.containers.volumeMounts.name*
    * *.spec.template.spec.volumes.name*

  This is a workaround to the issue mentioned at: https://github.com/kubernetes/kubernetes/issues/60046

## Installation

This driver must be deployed and installed on all nodes in the cluster.  The RPM installs the driver at /usr/libexec/kubernetes/kubelet-plugins/volume/exec/dell~scaleio/scaleio.  After installing the RPM on each node, reboot the nodes for the driver to take effect.

## Troubleshooting

This section covers some commonly encountered issues.  If they resemble what is being observed, see if the suggested action(s) help diagnose the issue.

* **SYMPTOM**:
  * Kubernetes/OpenShift is not using the driver.
  * Pods/deployments are starting up because they cannot access/mount the specified volume(s).
* **DIAGNOSTIC ACTION(S)**:
  * Ensure /usr/libexec/kubernetes/kubelet-plugins/volume/exec/dell~scaleio/scaleio exists on every node in the cluster, and has executable permissions.
  * Ensure /opt/emc/scaleio/flexvolume/bin/get-token.sh exists on every node in the cluster, and has executable permissions.
  * Ensure the config file specified by the *KUBCONFIG* global variable in /opt/emc/scaleio/flexvolume/cfg/config exists on every node in the cluster, and has executable permissions.
  * Ensure /opt/emc/scaleio/flexvolume/bin/get-token.sh can be run directly on every node in the cluster, and outputs a token to stdout.


* **SYMPTOM**:
  * /opt/emc/scaleio/flexvolume/bin/get-token.sh does not output a token to stdout.
* **DIAGNOSTIC ACTION(S)**:  
  * Ensure the config file specified by the *KUBCONFIG* global variable in /opt/emc/scaleio/flexvolume/cfg/config provides sufficient access to obtain information about the service account specified by the *SERVICE_ACC* global variable in /opt/emc/scaleio/flexvolume/cfg/config.  More specifically, confirm that `[kubectl|oc] --config=<KUBECONFIG> get sa <SERVICE_ACC>` outputs secret information about the service account.


* **SYMPTOM**:
  * After deleting a persistent volume and pod, Kubernetes/OpenShift continually calls the driver's getvolumename() function every second.
* **DIAGNOSTIC ACTION(S)**:
  * Ensure Kubernetes/OpenShift successfully detaches the persistent volume from the pod (which occurs during pod deletion) before deleting the persistent volume itself.  More specifically, on the master node, look for messages such as the following in /var/log/messages:
    * ``origin-master-controllers: ... Verified volume is safe to detach for volume "<volumeID>" (UniqueName: "flexvolume-dell/scaleio/<volumeID>") on node ...``
    * ``origin-master-controllers: ... DetachVolume.Detach succeeded for volume "<volumeID>" (UniqueName: "flexvolume-dell/scaleio/<volumeID>") on node ...``
  * To address the issue, once encountered, reboot the node(s).

