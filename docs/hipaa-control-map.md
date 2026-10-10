# HIPAA Security Rule alignment map

ClinicGuard is an educational lab and does not establish HIPAA compliance.
The data is synthetic, and the controls below are demonstrations of security
concepts rather than a formal risk assessment or attestation.

| Security concept | ClinicGuard implementation | Evidence |
| --- | --- | --- |
| Access control | Default-deny nftables policy with explicit staff HTTPS access | `gateway/nftables.conf`, `tests/test_policy.py` |
| Network isolation | Separate internal Docker networks for each trust zone | `docker-compose.yml`, ADR 001 |
| Transmission security | TLS between staff and the gateway, and gateway and EHR proxy | `gateway/nginx.conf`, `ehr/nginx.conf` |
| Audit controls | nginx access/error logs and Suricata `eve.json` shipped to Loki | `monitoring/promtail/config.yml` |
| Integrity/configuration control | Git-tracked Compose, firewall, tests, and CI validation | `.github/workflows/ci.yml` |
| Incident detection | Suricata local rules and Grafana log dashboard | `monitoring/suricata/local.rules`, Grafana provisioning |
| Minimum necessary access | Client-specific routes and narrowly scoped firewall rules | `clients/entrypoint.sh`, `gateway/nftables.conf` |

Production use would additionally require organizational policies, workforce
training, key management, vulnerability management, backups, documented risk
analysis, and many controls outside this repository.
