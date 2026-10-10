#!/bin/sh
set -eu

backup_dir="${1:-./backups/$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "$backup_dir"

docker compose cp ehr-app:/var/lib/clinicguard/ehr.sqlite3 "$backup_dir/ehr.sqlite3"
docker compose cp loki:/loki "$backup_dir/loki"
docker compose cp grafana:/var/lib/grafana "$backup_dir/grafana"

printf 'ClinicGuard backup written to %s\n' "$backup_dir"
