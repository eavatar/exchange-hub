FROM eavatar/hub-runtime

ADD src/eavatar.x.hub /app/code/
WORKDIR /app
EXPOSE 5000
CMD ["/app/launcher"]