#!/bin/bash

# This script takes etcd configuration from environment variables and builds a etcd configuration file.
set -e

# we are not using parsing the argument from the DOCKERFILE
CONFIG="/etc/etcd.conf.yml"

# Generate the config only if it doesn't exist
if [[ ! -f "${CONFIG}" ]]; then

    {
        echo "name: '${NODE_NAME}'"
        echo "data-dir: '/var/lib/etcd'" # zde si ukládá data
        echo "initial-advertise-peer-urls: 'http://${NODE_IP}:2380'" # adresa na které bude etcd dostupné pro ostatní servery
        echo "listen-peer-urls: 'http://0.0.0.0:2380'" # adresa na které bude etcd naslouchat
        echo "advertise-client-urls: 'http://${NODE_IP}:2379'" # adresa na které bude etcd dostupné pro klienty
        echo "listen-client-urls: 'http://0.0.0.0:2379'"
        # CLUSTER = ${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380
        echo "initial-cluster: '${CLUSTER}'" # seznam všech serverů v clusteru 
        echo "initial-cluster-state: 'new'" # stav clusteru, new pokud je to první server
        echo "initial-cluster-token: 'etcd-cluster'" # token pro identifikaci clusteru
    } >> "${CONFIG}"
fi

exec "$@"
