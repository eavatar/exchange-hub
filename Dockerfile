FROM eavatar/hub-runtime

ADD src/eavatar.x.hub /app/code/
WORKDIR /app

CMD ["/app/launcher"]