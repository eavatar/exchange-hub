FROM eavatar/hub-cooker
MAINTAINER sampot <sam@eavatar.com>

RUN git clone https://github.com/pyinstaller/pyinstaller.git /tmp/pyinstdev

ADD ./src /build/src
ADD ./package.spec /build/
RUN chown -R ava:ava /build

USER ava
WORKDIR /build
RUN python /tmp/pyinstdev/pyinstaller.py package.spec --clean -y

WORKDIR /build/dist/eavatar

RUN tar cf /build/hub.tar .