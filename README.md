# ClinicGuard

ClinicGuard is a simulated, monitored small-clinic network built with Docker
Compose. It demonstrates network segmentation, default-deny firewall policy,
TLS for a synthetic EHR application, centralized logging, IDS alerting, and
automated security-policy tests.

> This project uses synthetic data only. It is an educational lab and is not a
> HIPAA compliance certification or a production healthcare network.

## Status

Phase 1: architecture and repository scaffold.

## Planned zones

| Zone | Subnet | Purpose |
| --- | --- | --- |
| Staff | `10.10.10.0/24` | Trusted clinic workstations |
| Guest | `10.10.20.0/24` | Untrusted guest Wi-Fi clients |
| Server | `10.10.30.0/24` | Reverse proxy and synthetic EHR |
| Management | `10.10.99.0/24` | IDS and observability services |
| Attacker | `10.10.66.0/24` | Simulated external threat |

Docker networks simulate separate routed segments. They are not physical
802.1Q VLANs.

## Prerequisites

- Docker Desktop with WSL2 integration enabled
- Git
- WSL2

For the best bind-mount and filesystem behavior, keep the working copy inside
the WSL filesystem (for example, `~/src/clinicguard`) when running Docker.

## Planned commands

```bash
make up
make test
make attack
make down
```

See [docs/setup-guide.md](docs/setup-guide.md) for the Windows + WSL2 setup
notes and [docs/architecture.md](docs/architecture.md) for the design.

