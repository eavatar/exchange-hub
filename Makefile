
all: cooker packer shipper
	
cooker: builders/cooker/Dockerfile requirements.txt
	mkdir -p build/cooker
	rm -rf build/cooker/*
	cp requirements.txt build/cooker/
	cp builders/cooker/Dockerfile build/cooker/
	docker build -t eavatar/hub-cooker ./build/cooker


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
