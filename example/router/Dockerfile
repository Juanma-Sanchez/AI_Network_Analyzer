FROM ubuntu:latest

RUN apt update
RUN apt install -y frr frr-pythontools snmpd snmp libsnmp-dev iproute2 net-tools iputils-ping nano

COPY entrypoint.sh entrypoint.sh
COPY daemons /etc/frr/daemons
COPY frr.conf /etc/frr/frr.conf

#RUN chown -R frr:frr /etc/frr
#EXPOSE 2605

CMD ["sh", "entrypoint.sh"]