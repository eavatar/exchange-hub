GROUP=eavatar
NAME=exchange-hub
VERSION=0.1.0

all: build tag
	

runtime: src/eavatar.x.runtime/Makefile
	cp requirements.txt src/eavatar.x.runtime/overlayfs/
	cd src/eavatar.x.runtime && make clean all

build: Dockerfile
	docker build  -t $(GROUP)/$(NAME):$(VERSION) .

tag:
	@if ! docker images $(GROUP)/$(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	docker tag $(GROUP)/$(NAME):$(VERSION) $(GROUP)/$(NAME):latest