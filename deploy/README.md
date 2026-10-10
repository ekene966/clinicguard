# Production-style deployment notes

ClinicGuard is an educational lab. For an online demonstration, use a
hardened Linux VM rather than exposing Docker Desktop directly.

Before starting:

1. Set `EHR_DEMO_PASSWORD` and `GRAFANA_ADMIN_PASSWORD` in a protected `.env`.
2. Permit only SSH from an administrator IP and HTTPS from the internet.
3. Put a trusted TLS reverse proxy in front of Grafana.
4. Keep the EHR, Loki, Promtail, Suricata, and management networks private.
5. Schedule `make backup` and test restores.
6. Review container capabilities and remove `NET_ADMIN` where the lab does not
   require it.

The default `docker-compose.yml` remains the reproducible educational profile.
Do not treat it as a production healthcare deployment.
