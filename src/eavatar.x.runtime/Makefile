GROUP=eavatar
NAME=hub-runtime
VERSION=0.1.0


all: build tag

build: Dockerfile overlayfs.tar
	docker build --rm -t $(GROUP)/$(NAME):$(VERSION) .


overlayfs.tar:
	cd overlayfs && docker build -t $(NAME)-builder .
	docker run --rm $(NAME)-builder cat /build/overlayfs.tar > overlayfs.tar
	docker rmi $(NAME)-builder

tag:
	@if ! docker images $(GROUP)/$(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	docker tag $(GROUP)/$(NAME):$(VERSION) $(GROUP)/$(NAME):latest

clean:
	rm -f overlayfs.tar