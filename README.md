### Description
Check script to monitor the replica set status of a Kubernetes Deployment

---

### How it works
For a given deployment,  the number of ready pods is compared against the specified replics minus the Max Unavailable setting defined in the Rolling Update Strategy.  A metric of 'replicas' is ommited as performance data.

##### Results:
* OK: The number of ready pods exceeds the required number of pods
* WARNING: The number of ready pods is equal to the required number of pods
* ERROR:  The number of ready pods is below the required number of pods

---

### Usage
```console
user@host:~$ check-kube-deployment-replica-status.py -h
usage: check-kube-deployment-replica-status.py [-h] -d DEPLOYMENT
                                                 [-n NAMESPACE]
 
user@host:~$ check_kube_deployment_replicas -d deployment-foo -n namespace-bar
OK, test deployment has 8 pods ready of the 8 required | replicas=8

```
---

### Requirements
A working kubernetes configuration via either a config file at ~/.kube/config or the environment variable KUBECONFIG
 
##### Python libraries
* argparse
* kubernetes
