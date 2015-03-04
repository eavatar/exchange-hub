FROM eavatar/builder

#ENV DEBIAN_FRONTEND noninteractive
#RUN apt-get update
#RUN apt-get install -y python2.7 openssl python-pip python-virtualenv libffi-dev

RUN git clone https://github.com/pyinstaller/pyinstaller.git /tmp/pyinstdev

RUN mkdir -p /build
ADD ./src /build/src
ADD ./package.spec /build/
ADD requirements.txt /build/
RUN chown -R ava:ava /build
WORKDIR /build
RUN pip install -r requirements.txt

USER ava

RUN python /tmp/pyinstdev/pyinstaller.py package.spec --clean -y

WORKDIR /build/dist

RUN tar cf /build/overlayfs.tar .

