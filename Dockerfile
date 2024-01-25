# syntax=docker/dockerfile:1

FROM python:3.8

LABEL autor="Michal Goryszewski"
LABEL version="1.0.1"

WORKDIR /app

RUN apt update && apt  install mariadb-client -y

COPY ["req.txt" ,"./"]
RUN pip3 install -r req.txt

RUN apt update && apt install libvirt-clients libvirt-dev -y
RUN apt update && apt install python3-dev python3-libxml2 xml-core libxml2 libxml2-dev libxslt-dev -y
COPY ["req-test.txt" ,"./"]
RUN pip3 install -r req-test.txt
COPY . .
EXPOSE 8050

CMD [ "python3" ,"-m" ,"flask" , "--debug", "run" ]
