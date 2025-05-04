From ubuntu:25.04

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    sudo \
    ca-certificates \
    build-essential \
    libcurl4-openssl-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/WiringPi/WiringPi.git && \
    cd WiringPi && \
    ./build