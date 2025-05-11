FROM python:latest

RUN apt update
RUN apt install -y iproute2 net-tools iputils-ping nano vim
COPY requirements.txt requirements.txt
COPY host.py host.py
COPY data.json data.json
RUN pip install -r requirements.txt
CMD ["python", "host.py"]