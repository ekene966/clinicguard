#!/bin/sh
set -u

echo "ClinicGuard attack simulation"
for target in 10.10.10.254 10.10.20.254 10.10.30.10 10.10.99.254; do
  if wget --no-check-certificate -qO- --timeout=2 "https://${target}/" >/dev/null 2>&1; then
    echo "UNEXPECTEDLY REACHED ${target}:443"
  else
    echo "BLOCKED ${target}:443"
  fi
done
