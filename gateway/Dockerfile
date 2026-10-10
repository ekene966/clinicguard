FROM alpine:3.20

RUN apk add --no-cache nftables dnsmasq iproute2 tcpdump nginx openssl

COPY entrypoint.sh /entrypoint.sh
COPY nftables.conf /etc/nftables.conf
COPY nginx.conf /etc/nginx/http.d/clinicguard.conf
RUN chmod 0755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
