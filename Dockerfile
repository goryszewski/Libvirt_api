# syntax=docker/dockerfile:1

FROM python:3.8

LABEL autor="Michal Goryszewski"
LABEL version="1.0.1"

WORKDIR /app

RUN apt update && apt  install mariadb-client -y

COPY ["req.txt" ,"./"]
RUN pip3 install -r req.txt

COPY . .
EXPOSE 8050

CMD [ "python3" ,"-m" ,"flask" , "--debug", "run" ]

# podman develop
# docker run --rm -p 5000:5000 -it -v .:/app  --security-opt label=disable b375b42f7d91
