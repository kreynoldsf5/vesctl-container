FROM alpine:latest

ADD vesctl.linux-amd64.gz /tmp/

RUN gunzip /tmp/vesctl.linux-amd64.gz &&\
    mv /tmp/vesctl.linux-amd64 /opt/vesctl &&\
    chmod +x /opt/vesctl

ENV PATH="/opt/:$PATH" 
ENTRYPOINT ["/opt/vesctl"]