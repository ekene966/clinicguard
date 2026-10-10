# ClinicGuard threat model

This model describes the threats simulated by the lab. It is intentionally
small and uses synthetic data only.

| Asset | Threat | Control | Evidence |
| --- | --- | --- | --- |
| Synthetic EHR | Guest or attacker reaches patient-record application | Staff-only gateway HTTPS policy and default-deny forwarding | `tests/test_policy.py` |
| EHR traffic | Network eavesdropping | TLS at the gateway and EHR reverse proxy | `gateway/nginx.conf`, `ehr/nginx.conf` |
| Staff access | Unauthorized internal access | Separate staff, guest, server, and attacker networks | `docker-compose.yml` |
| Gateway | Configuration bypass | Internal Docker networks and Git-tracked nftables policy | ADR 001 and ADR 002 |
| Network activity | Reconnaissance or probing | Suricata rules and centralized logs | `monitoring/suricata/local.rules`, Grafana |
| Audit evidence | Logs unavailable during investigation | Promtail and Loki with named persistent volumes | `monitoring/promtail/config.yml` |

## Out of scope

This lab does not model real switches, 802.1Q VLANs, identity providers,
endpoint management, physical security, backups, disaster recovery, or real
PHI. It also does not claim that a Docker simulation satisfies HIPAA.

## Residual risks

The lab uses self-signed certificates, fixed demonstration IP addresses, and
container capabilities required for routing and packet inspection. A
production deployment would need managed certificates, centralized identity,
key rotation, vulnerability management, hardened hosts, and formal risk
analysis.
