# Dockerfile.app

# Multi Stage Build mit NTFY
FROM debian:stable-20230411-slim AS NTFY

# Setzen der NTFY_VERSION-Umgebungsvariablen
ARG NTFY_VERSION=2.3.1
ENV NTFY_VERSION=${NTFY_VERSION}

WORKDIR /NTFY

# Installieren von ntfy und notwendigen Tools
RUN apt-get update 
RUN apt-get install -y wget 
RUN wget https://github.com/binwiederhier/ntfy/releases/download/v${NTFY_VERSION}/ntfy_${NTFY_VERSION}_linux_amd64.deb

FROM python:3.11-slim-bullseye

RUN apt-get update 
RUN apt-get install -y wget 

COPY --from=NTFY /NTFY/ntfy_*.deb ./

RUN dpkg -i ntfy_*.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* ntfy_*.deb

RUN apt-get update && \
    apt-get install -y wget procps gnupg lsb-release && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli


RUN pip install requests

# Setzen des Arbeitsverzeichnisses
WORKDIR /src

# Kopieren des Skripts in den Container
COPY src/very_simple_start_skript.py /src/very_simple_start_skript.py

HEALTHCHECK  --interval=5s --timeout=3s \
  CMD pgrep -f "very_simple_start_skript.py" || exit 1

# Standardkommando, das beim Start des Containers ausgeführt wird
CMD ["python3", "-u", "very_simple_start_skript.py"]
