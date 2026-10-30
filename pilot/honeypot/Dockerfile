FROM python:3.11-slim
RUN mkdir -p /var/log/honeypot
COPY honeypot.py /srv/honeypot.py
ENTRYPOINT ["python", "/srv/honeypot.py"]
