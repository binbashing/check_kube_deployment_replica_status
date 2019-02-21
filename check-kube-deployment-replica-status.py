#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Python script used to check the replicaset status of a given deployment
"""

import argparse
from kubernetes import client, config

# Parse arguements
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--deployment',
                    help='Name of deployment to check',
                    required=True)
parser.add_argument('-n', '--namespace',
                    help='Namespace for deployment',
                    required=False,
                    default='default')
args = parser.parse_args()
deployment = (args.deployment)
namespace = (args.namespace)

# Load kube.cong
config.load_kube_config()

# Establish connection to Kubernetes
kube_conn = client.AppsV1Api()


# Helper function to convert percentage to integer
def max_unavail_calc(max_unavailable, replicas_specd):
    return int(replicas_specd * (float(max_unavailable.strip('%')) / 100.0))

# Get Specs and Status of Deployment
response = kube_conn.read_namespaced_deployment_status(deployment, namespace)
replicas_specd = response.spec.replicas
max_unavailable = response.spec.strategy.rolling_update.max_unavailable
if '%' in max_unavailable:
    max_unavailable = max_unavail_calc(max_unavailable, replicas_specd)
replicas_reqd = replicas_specd - max_unavailable
replicas_ready = response.status.ready_replicas

# Build response message
status_msg = (
    '{} deployment has {} pods ready of the {} required replicas={}'.
    format(deployment, replicas_ready, replicas_reqd, replicas_ready)
    )

# Perform check
if replicas_ready > replicas_reqd:
    print('OK, {}'.format(status_msg))
    exit(0)
elif replicas_ready == replicas_reqd:
    print('WARNING, {}'.format(status_msg))
    exit(1)
else:
    print('ERROR, {}'.format(status_msg))
    exit(2)
