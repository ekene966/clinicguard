#!/bin/sh
set -eu

echo "ClinicGuard gateway started with forwarding enabled."
nft -f /etc/nftables.conf
exec sleep infinity
