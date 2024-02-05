FROM alpine:3.15

COPY appdata /appdata

ENV filename=None
ENV outfile=None
ENV multiple=False
ENV pretty=False
ENV sortkey=False
ENV defaultkey=None
ENV appicons=True
ENV appicondir=/
ENV outfiledir=/

WORKDIR /home/work/

RUN apk update
RUN apk upgrade
RUN apk add bash nano python3 python2

ENTRYPOINT /usr/bin/python3 /appdata/ipax.py $filename $outfile $multiple $pretty $sortkey $defaultkey $appicons $appicondir $outfiledir
