#!/bin/sh
set -eu

case "${1:-}" in
  staff) gateway="10.10.10.254" ;;
  guest) gateway="10.10.20.254" ;;
  attacker) gateway="10.10.66.254" ;;
  *) echo "usage: $0 {staff|guest|attacker}" >&2; exit 64 ;;
esac

ip route replace default via "$gateway"
echo "Client route configured through $gateway"
exec sleep infinity
