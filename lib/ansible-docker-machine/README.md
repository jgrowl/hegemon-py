# ansible-docker-machine
An experimental ansible module for docker-machine.

I am not sure if this will work out well or be that useful. I am just playing around with the idea.

Example task:

    - docker_machine: name=testMachine driver=digitalocean access_token=xxxxxxxx state=running

