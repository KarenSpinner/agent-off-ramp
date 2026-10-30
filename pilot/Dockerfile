FROM python:3.11-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends inotify-tools curl ca-certificates procps \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest==8.3.3 inspect-tool-support \
 && inspect-tool-support post-install --no-web-browser
# File-activity monitor runs under a plain name so `ps` does not advertise it.
RUN cp /usr/bin/inotifywait /usr/lib/sysaudit && mkdir -p /var/lib/.sysaudit /workspace
WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
