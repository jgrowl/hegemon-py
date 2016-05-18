#!/usr/bin/env sh
set -e

if [ -z "$HEGEMON_UID" ]; then
#    echo 'Using default uid'
    echo ''
else
    usermod -u $HEGEMON_UID hegemon
fi

if [ -z "$HEGEMON_GID" ]; then
    echo ''
#    echo 'Using default gid'
else
    groupmod -g $HEGEMON_GID hegemon
fi

# I'd like a better way to do this. I don't really want to alter keep_var either
sudo HEGEMON_SHELL=$HEGEMON_SHELL \
    ANSIBLE_LIBRARY=$ANSIBLE_LIBRARY \
    HEGEMON_LIB_HOME=$HEGEMON_LIB_HOME \
    ANSIBLE_CONFIG=$ANSIBLE_CONFIG \
    PATH=$PATH  \
    PYTHONPATH=$PYTHONPATH \
    -u hegemon -s /opt/hegemon/bin/hegemon $@

