FROM postgres:17-bookworm AS builder

RUN apt -y update && \
    apt install -y python3.11 python3-pip postgresql-server-dev-17 && \
    pip3 install build --break-system-packages


RUN mkdir /tmp/build
COPY multicorn2 /tmp/build/multicorn2
WORKDIR /tmp/build/multicorn2
RUN make PYTHON_OVERRIDE=python3.11
RUN make PYTHON_OVERRIDE=python3.11 install
ENV POSTGRES_HOST_AUTH_METHOD=trust
RUN python3 -m build -w -n
RUN pip3 install --break-system-packages dist/*whl
