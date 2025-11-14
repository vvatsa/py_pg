FROM postgres:17-bookworm AS builder

RUN apt -y update && \
    apt install -y python3.11 python3-pip postgresql-server-dev-17 && \
    pip3 install build --break-system-packages


RUN mkdir /tmp/build
COPY multicorn2 /tmp/build/multicorn2
WORKDIR /tmp/build/multicorn2
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV PYTHON_OVERRIDE=python3.11
RUN make
RUN make install

COPY pgvector /tmp/build/pgvector
WORKDIR /tmp/build/pgvector
RUN make
RUN make install

COPY . /tmp/build
WORKDIR /tmp/build

RUN python3 -m build -w -n
RUN pip3 install --break-system-packages dist/*whl
ADD init.sql /docker-entrypoint-initdb.d/init.sql
