#!/usr/bin/env sh
set -e

if [ -z "$HEGEMON_UID" ]; then
    break
else
    usermod -u $HEGEMON_UID hegemon
fi

if [ -z "$HEGEMON_GID" ]; then
    break
else
    groupmod -g $HEGEMON_GID hegemon
fi

# I'd like a better way to do this. I don't really want to alter keep_var either
sudo ANSIBLE_LIBRARY=$ANSIBLE_LIBRARY \
    HEGEMON_LIB_HOME=$HEGEMON_LIB_HOME \
    PATH=$PATH  \
    PYTHONPATH=$PYTHONPATH \
    -u hegemon -s /opt/hegemon/lib/hegemon-core/exe/hegemon $@
