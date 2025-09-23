FROM postgres:17-bookworm AS builder

RUN apt -y update && \
    apt install -y python3.11 python3-pip postgresql-server-dev-17


RUN mkdir /tmp/build
COPY multicorn2 /tmp/build/multicorn2
WORKDIR /tmp/build/multicorn2
RUN make PYTHON_OVERRIDE=python3.11
RUN make PYTHON_OVERRIDE=python3.11 install
