FROM alpine:latest

COPY appdata /appdata

ENV filename=none

WORKDIR /home/work/

RUN apk update
RUN apk upgrade
RUN apk add bash nano python3 python2 libplist-util

ENTRYPOINT /usr/bin/python3 /appdata/ipax.py $filename
