# hegemon
An opinionated infrastructure management and orchestration framework built on top of ansible and docker


## What is this?

This project provides a complete website infrastructure. The goal is to have a generic skeleton for complete infrastructure management. It's all dependent on Docker containers.

## What can I do with it?

Through flat configuration files, you can create an entire production infrastructure with multiple pluggable services.

## Raison D'être

Managing website infrastructure, configuration, and secrets is painful. Stuff is spread everywhere, you may forget where things are, such as IP addresses or how you configured something. You might have moved something to another server or not remember how things are done. When you have a system with even a single node, it can be frustrating managing what's on it. It gets exponentially more difficult when you have multiple nodes and you try to have fault tolerance, logging, and service discovery across all nodes.

This project lets you manage an entire system of servers and services through one location, just in text files. It's intended to be easy to understand and search through, easy to scale up and down to support production-level systems as well as simple systems.

## How do I use it?

### Dependencies

- docker
- pip

### Installation

    pip install -r ./requirements.txt
    
### Running

Clone repository

    mkdir /opt/hegemon && (cd /opt/hegemon; git clone https://github.com/jgrowl/hegemon.git)

Set `HEGEMON_LIB_HOME` to wherever you install hegemon

    export HEGEMON_LIB_HOME=/opt/hegemon/lib/hegemon-core/lib
    alias hegemon=/opt/hegemon/lib/hegemon-core/exe/hegemon
    
Create new project

    hegemon new <name>

### Inventories Folder

This contains specific environment configuration, e.g., development and production. Most of the configuration lies in this folder. Inside each environment, define:

1. The process in which you bring up Docker hosts. You can use Docker machine for example.
1. A hosts file, like in Ansible. The hosts file defines what you're putting on each host, e.g., a mail server on server X, a web server on server Y.
1. There's a host\_vars folder, like in Ansible. It contains variables for each host.

There's a configuration file at config/_yourEnvironment_/host\_vars/setup\_hosts.yml. Edit this file and fill in your Digital Ocean access token. This is just for the included example, you could use Amazon EC2 or some other service.

## Notes

By default hegemon will start a new container, run, and then clean up after itself. The --skip-container flag can be used to skip this step but there may be modifications or other destructive actions taken on your computer! This is not recommended at this time!


## Development

### Build hegemon image

    make
