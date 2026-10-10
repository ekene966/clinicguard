FROM alpine:3.20

RUN apk add --no-cache nftables dnsmasq iproute2 tcpdump

COPY entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

