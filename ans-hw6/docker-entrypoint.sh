#!/bin/bash
set -e

if [ -d "/root/.ssh-mounted" ]; then
    rm -rf /root/.ssh
    mkdir -p /root/.ssh
    chmod 700 /root/.ssh
    
    cp -r /root/.ssh-mounted/* /root/.ssh/ 2>/dev/null || true
    
    find /root/.ssh -type f -name "id_*" ! -name "*.pub" -exec chmod 600 {} \;
    find /root/.ssh -type f -name "*.pub" -exec chmod 644 {} \;
    
    cat > /root/.ssh/config << EOF
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
EOF
    chmod 600 /root/.ssh/config
fi

exec "$@"