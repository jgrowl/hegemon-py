.PHONY: all build

IMAGE_NAME=jgrowl/hegemon

all: build

build:
	docker build -t $(IMAGE_NAME) .

#shell: build
#	docker run --rm -it --name=site_bootstrap_hegemon $(IMAGE_NAME)
