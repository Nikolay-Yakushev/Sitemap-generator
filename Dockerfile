FROM ubuntu:18.04
RUN apt update
RUN apt install -y python3.8 python3-pip
RUN pip3 install bs4 requests urllib3 PyYaml lxml psycopg2-binary
RUN apt install vim -y 
COPY Sitemap-generator /home/sitemap

