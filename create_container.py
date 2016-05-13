from docker import Client
cli = Client(base_url='tcp://127.0.0.1:2375')
container = cli.create_container(image='busybox:latest', command='/bin/sleep 30')