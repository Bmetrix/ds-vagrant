#
# Simple backend demo server image
#

# pokud cista kontejner pak prikaz FROM scratch -> tak ziskame uplne novej, cistej konterner
FROM ghcr.io/maxotta/kiv-dsa-vagrant-base-docker:latest

# -q -> quiet; -y -> yes
RUN yum -q -y install python3
RUN yum -q -y install python3-pip
# flask pro web server v pythonu 
RUN pip3 install flask

# copy directory python to /opt/backend
# pokud na backend dame prikaz ls -lR /opt/backend/ tak tam uvidime simple-backend.py
COPY python /opt/backend

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 CMD curl -s http://localhost:5000/ping | grep pong

# what to start when docker starts container
CMD /usr/bin/python3 /opt/backend/simple-backend.py

# EOF
