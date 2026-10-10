#!/bin/sh
set -eu

ip route replace default via 10.10.30.254
exec python3 /app.py
