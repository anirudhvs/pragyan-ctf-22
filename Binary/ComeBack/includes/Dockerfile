FROM nsjail

COPY ./vuln /home/ctf/chal/
COPY ./libvuln.so /home/ctf/chal
COPY ./flag /home/ctf/chal/
EXPOSE 5663/tcp
CMD ["/chal/vuln"]
