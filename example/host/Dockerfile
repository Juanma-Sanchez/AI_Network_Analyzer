FROM python:latest

RUN apt update
RUN apt install -y iproute2 net-tools iputils-ping
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["tail", "-f", "/dev/null"]