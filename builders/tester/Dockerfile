FROM eavatar/hub-cooker

ADD ./requirements.txt /
ADD ./scripts /scripts
WORKDIR /scripts
RUN pip install -r /requirements.txt

CMD ["nosetests"]

