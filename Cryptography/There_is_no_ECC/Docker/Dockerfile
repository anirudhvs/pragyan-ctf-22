FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get -y install --no-install-recommends autoconf bison flex gcc g++ git libprotobuf-dev libnl-route-3-dev libtool make pkg-config protobuf-compiler && \
    git config --global http.sslverify false && \
    git clone https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && make && cd / && \
    mv /nsjail/nsjail /bin && \
    rm -r /nsjail && \
    dpkg --add-architecture i386 && \
    apt-get update && apt-get -y --no-install-recommends install libc6-i386 libprotobuf-dev libnl-route-3-200 protobuf-compiler libgmp3-dev && \
    useradd -r -m -u 1000 ctf

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/local/lib

COPY app /home/ctf/app
COPY startup.sh /home/ctf

WORKDIR /home/ctf/app
RUN g++ -static chall.cpp -o chall -lgmp

WORKDIR /home/ctf
RUN chmod +x startup.sh && \
    chown -R ctf: .
