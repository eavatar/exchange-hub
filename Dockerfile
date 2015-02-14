FROM eavatar/hub-runtime

ADD src/eavatar.hub /app/code/
WORKDIR /app

CMD ["/app/launcher"]