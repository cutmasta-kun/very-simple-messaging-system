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

RUN pip install requests

# Kopieren der Skripte

COPY src/ /src

# Setzen des Arbeitsverzeichnisses
WORKDIR /src

HEALTHCHECK  --interval=5s --timeout=3s \
  CMD pgrep -f "very_simple_start_skript.py" || exit 1

# Standardkommando, das beim Start des Containers ausgeführt wird
CMD ["python3", "-u", "very_simple_start_skript.py"]
