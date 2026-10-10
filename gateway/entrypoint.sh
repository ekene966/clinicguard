#!/bin/sh
set -eu

echo "ClinicGuard gateway started with forwarding enabled."
sysctl -w net.ipv4.ip_forward=1 >/dev/null
nft -f /etc/nftables.conf
exec sleep infinity
