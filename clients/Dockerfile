FROM alpine:3.20

RUN apk add --no-cache iproute2 iputils curl

COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
