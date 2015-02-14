GROUP=eavatar
NAME=exchange-hub
VERSION=0.1.0

all: build tag
	
cooker: builders/cooker/Dockerfile requirements.txt
	mkdir -p build/cooker
	rm -rf build/cooker/*
	cp requirements.txt build/cooker/
	cp builders/cooker/Dockerfile build/cooker/
	docker build -t eavatar/hub-cooker ./build/cooker

dist/hub.tar: packer

packer: builders/packer/package.spec packer/Dockerfile
	mkdir -p build/packer
	rm -rf build/packer/*
	cp builders/packer/Dockerfile build/packer/
	cp builders/packer/package.spec build/packer/
	cp -a src build/packer/
	docker build -t eavatar/hub-packer ./build/packer
	docker run  eavatar/hub-packer cat /build/hub.tar > dist/hub.tar


shipper: builders/shipper/Dockerfile dist/hub.tar
	mkdir -p build/shipper
	rm -rf build/shipper/*
	cp builders/shipper/Dockerfile build/shipper/
	cp dist/hub.tar build/shipper/
	docker build -t eavatar/hub ./build/shipper


tester: builders/tester/Dockerfile
	docker build -t eavatar/hub-tester ./tester

runtime: src/eavatar.app-runtime/Makefile
	cd src/eavatar.app-runtime && make clean all

build: Dockerfile
	docker build  -t $(GROUP)/$(NAME):$(VERSION) .

tag:
	@if ! docker images $(GROUP)/$(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	docker tag $(GROUP)/$(NAME):$(VERSION) $(GROUP)/$(NAME):latest