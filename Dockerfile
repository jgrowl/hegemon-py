FROM generik/ansible:v2.0
MAINTAINER Jonathan Rowlands <jonrowlands83@gmail.com>

RUN apk --update --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted add curl ca-certificates docker python3 sudo && \
    apk --update --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted add shadow && \
    curl -Ls https://circle-artifacts.com/gh/andyshinn/alpine-pkg-glibc/6/artifacts/0/home/ubuntu/alpine-pkg-glibc/packages/x86_64/glibc-2.21-r2.apk > /tmp/glibc-2.21-r2.apk && \
    apk add --allow-untrusted /tmp/glibc-2.21-r2.apk && \
    rm -rf /tmp/glibc-2.21-r2.apk /var/cache/apk/*

RUN pip install docker-py docopt dockerpty

# This is some temporary ugliness until --devices gets added to docker command in 2.1
RUN cd /opt/ansible/ansible && git checkout devel && git pull && git checkout stable-2.1
RUN cd /opt/ansible/ansible/lib/ansible/modules/core && git checkout devel && git pull && git checkout stable-2.1
#RUN cd /opt/ansible/ansible/lib/ansible/modules/extra && git checkout stable-2.1

## Fix
#RUN cd /opt/ansible/ansible/lib/ansible/modules/core && wget https://github.com/kaczynskid/ansible-modules-core/commit/46970d6d7add50780e8cedb5067ae5d29a763141.patch -O docker-fix.patch
#RUN cd /opt/ansible/ansible/lib/ansible/modules/core && git apply docker-fix.patch

# Put required unmanaged dependencies here
RUN mkdir -p /usr/local/bin

RUN curl -L https://github.com/docker/machine/releases/download/v0.6.0/docker-machine-`uname -s`-`uname -m` > /usr/local/bin/docker-machine && \
    chmod +x /usr/local/bin/docker-machine

ENV PATH /usr/local/bin:$PATH

# Need to specify where you installed HEGEMON_LIB_HOME and ANSIBLE
ADD . /opt/hegemon
ENV HEGEMON_LIB_HOME /opt/hegemon
ENV ANSIBLE_LIBRARY /opt/hegemon/lib/ansible/library

# Ensure default ansible paths exist
#RUN mkdir -p /opt/ansible/ansible/library
#RUN mkdir -p /usr/share/ansible/plugins/connection_plugins
#RUN mkdir -p /etc/ansible/playbooks

# Hosts should always be specified in HEGEMON_HOME
RUN rm /etc/ansible/hosts

# Can't link in module_utils yet!
# see lib/ansible/module_utils/README
ADD ./lib/ansible-docker-machine/module_utils/docker_machine.py /opt/ansible/ansible/lib/ansible/module_utils/docker_machine.py

RUN groupadd -r hegemon && useradd -r -m -g hegemon hegemon

ENTRYPOINT ["/opt/hegemon/entrypoint.sh"]
