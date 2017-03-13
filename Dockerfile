FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install python-setuptools python-dev build-essential wget
RUN wget http://curl.haxx.se/ca/cacert.pem
RUN mkdir -p /etc/pki/tls/certs && mv cacert.pem /etc/pki/tls/certs/ca-bundle.crt
RUN easy_install pip
RUN pip install tensorflow tflearn scipy
ADD . /localfiles