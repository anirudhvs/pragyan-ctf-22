#!/bin/bash

# default file for pwn challenges
# alternative launch script can be specified via cmd in challenge dockerfile

PORT=${PORT:-3000}
MAX_CONNS_PER_IP=${MAX_CONNS_PER_IP:-0}
# 128MB
MAX_MEMORY=${MAX_MEMORY:-134217728}
MAX_PIDS=${MAX_PIDS:-16}
# 600 seconds
TIME_LIMIT=${TIME_LIMIT:-600}
RLIMIT_CPU=${RLIMIT_CPU:-20}

mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown -R ctf /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
nsjail \
    -Ml --port $PORT \
    --keep_env \
    --user ctf \
    --group ctf \
    --max_conns_per_ip $MAX_CONNS_PER_IP \
    -R /lib \
    -R /lib64 \
    -R /bin \
    -R /usr \
    -T /tmp \
    -T /dev -R /dev/urandom -R /dev/null \
    -R /home/ctf/app:/app \
    -D /app \
    --disable_proc \
    --time_limit $TIME_LIMIT \
    --rlimit_cpu $RLIMIT_CPU \
    --rlimit_as $MAX_MEMORY \
    --cgroup_pids_max $MAX_PIDS \
    --cgroup_mem_max $MAX_MEMORY \
    -- /app/app.py
