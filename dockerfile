FROM python:2.7
LABEL maintainer="Matthias Liffers <m@tthi.as>"

VOLUME /config

COPY . /pvstats

RUN pip install ./pvstats

CMD ["/pvstats/bin/pvstats", "--cfg", "/config/pvstats.conf"]
