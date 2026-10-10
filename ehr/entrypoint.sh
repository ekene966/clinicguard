#!/bin/sh
set -eu

mkdir -p /etc/nginx/certs
openssl req -x509 -nodes -newkey rsa:2048 -days 30 \
  -subj "/CN=clinicguard-ehr" \
  -keyout /etc/nginx/certs/ehr.key \
  -out /etc/nginx/certs/ehr.crt \
  >/dev/null 2>&1

exec nginx -g "daemon off;"
