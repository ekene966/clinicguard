# ClinicGuard

[![ClinicGuard checks](https://github.com/ekene966/clinicguard/actions/workflows/ci.yml/badge.svg)](https://github.com/ekene966/clinicguard/actions/workflows/ci.yml)
[![Security scans](https://github.com/ekene966/clinicguard/actions/workflows/security.yml/badge.svg)](https://github.com/ekene966/clinicguard/actions/workflows/security.yml)

ClinicGuard is a simulated, monitored small-clinic network built with Docker
Compose. It demonstrates network segmentation, default-deny firewall policy,
TLS for a synthetic EHR application, centralized logging, IDS alerting, and
automated security-policy tests.

> This project uses synthetic data only. It is an educational lab and is not a
> HIPAA compliance certification or a production healthcare network.

## What is implemented

Staff reach the gateway EHR proxy over HTTPS on TCP 443. The gateway proxies
to the EHR through its server-zone interface. Guest and attacker traffic is
denied by default. Suricata, Loki, Promtail, and Grafana provide centralized
security evidence, while pytest proves the access policy.

The synthetic EHR includes SQLite-backed users and patient records, PBKDF2
password verification, short-lived secure sessions, doctor/nurse/admin role
checks, audit events, JSON validation, and a `/healthz` endpoint. The default
lab password is controlled by `EHR_DEMO_PASSWORD`; set it in a local `.env`
file before sharing the stack.

The observability stack includes Loki, Promtail, and Grafana. Run
`make attack` to exercise blocked HTTPS probes and inspect the resulting logs.
See the [threat model](docs/threat-model.md) and
[HIPAA alignment map](docs/hipaa-control-map.md) for scope and limitations.

## About the application

ClinicGuard is a security engineering portfolio application rather than a
patient-facing medical product. It creates a small clinic environment with
separate staff, guest, server, management, and attacker trust zones. A staff
client reaches a synthetic EHR through the gateway's HTTPS reverse proxy.
Guest and attacker clients exercise denied paths, while Suricata, Loki,
Promtail, and Grafana collect evidence that the controls are working.

The EHR contains synthetic data only. No real patient records, authentication
system, billing workflow, or external healthcare integration is included.

## Technology stack

| Area | Technology | Version or role |
| --- | --- | --- |
| Runtime | Docker Desktop + Docker Compose | Linux containers on Windows/WSL2 |
| Gateway | Alpine Linux, nftables, nginx | Routing, firewall, TLS boundary |
| EHR | nginx + synthetic HTTP backend | TLS reverse proxy and demo service |
| IDS | Suricata | `7.0` image series; local detection rules |
| Logs | Loki + Promtail | `3.2.1`; centralized log collection |
| Dashboards | Grafana | `11.3.1`; provisioned Loki dashboard |
| Tests | Python + pytest | Python `3.12`; policy integration tests |
| Automation | GNU Make + GitHub Actions | Repeatable commands and CI |

The repository uses these languages and configuration formats:

- **Python** for integration tests.
- **POSIX shell** for container entrypoints and attack simulation.
- **nginx configuration** for TLS reverse proxies and access logs.
- **nftables configuration** for the default-deny firewall.
- **YAML** for Docker Compose, Promtail, Grafana provisioning, and CI.
- **JSON** for the Grafana dashboard.
- **Markdown** for architecture, setup, threat-model, and control documentation.

The version numbers above describe the pinned images and tools used during
validation. Check the image tags in [docker-compose.yml](docker-compose.yml)
when upgrading dependencies.

## Network zones

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

## Quick start

```bash
make up
make test
make attack
make down
```

Open Grafana at <http://localhost:3000> after `make up`.

See [docs/setup-guide.md](docs/setup-guide.md) for Windows + WSL2 setup notes
and [docs/architecture.md](docs/architecture.md) for the design.

## GitHub Pages site

The repository also publishes a static project overview through GitHub Pages:
<https://ekene966.github.io/clinicguard/>.

GitHub Pages hosts the portfolio site and documentation summary. It does not
run Docker, Grafana, Suricata, Loki, or the synthetic EHR; those services run
locally with Docker Compose. Updates to `site/` on `main` deploy automatically
through [.github/workflows/pages.yml](.github/workflows/pages.yml).

## How to update the project

Use a feature branch for changes and keep the default-deny policy intact:

```bash
git switch -c feat/short-description
# edit the relevant service, rule, test, or documentation
docker compose config
make test
make attack
git diff --check
git add .
git commit -m "feat: describe the change"
git push -u origin feat/short-description
```

Open a pull request after the local checks pass. GitHub Actions repeats Compose
validation, builds the stack, runs the policy tests, runs the attack
simulation, and tears the stack down even when a check fails. For a firewall
or network change, update the related test and one of
[docs/architecture.md](docs/architecture.md),
[docs/threat-model.md](docs/threat-model.md), or the relevant ADR.

## Feature roadmap

Good next improvements, in increasing scope:

1. Replace self-signed certificates with a local development CA and rotate
   certificates during tests.
2. Add Grafana alert rules for repeated blocked probes and Suricata signatures.
3. Add API-level tests for additional EHR authorization and audit logging cases.
4. Add a production-oriented deployment example using Kubernetes network
   policies, external secrets, and managed identity.
5. Add an active DHCP/DNS service and tests for lease assignment and name
   resolution. `dnsmasq` is currently installed in the gateway image but is
   not started, so DHCP/DNS is intentionally not claimed as implemented.

## Release roadmap

- **v0.2.0 — Hardening:** health checks, security headers, secret scanning,
  and Python security linting. **Released.**
- **v0.3.0 — EHR security:** authenticated users, roles, audit events,
  validation, and a persistent synthetic database. **Released.**
- **v0.4.0 — Operations:** backups, resource controls, and production-style
  deployment guidance. **Released.**
- **v1.0.0 — Advanced security:** image scanning, contribution tooling,
  releases, and expanded portfolio evidence. **Released.**

See [CHANGELOG.md](CHANGELOG.md) for completed release notes.

Operational helpers are in [deploy/](deploy/) and [scripts/](scripts/).
`make backup` captures the synthetic EHR database, Loki data, and Grafana
state for restore exercises.

## Reproducible evidence

The checks below execute against the running stack; they are not manually
typed status claims:

```bash
make up
make test
make attack
make down
```

`make test` covers staff HTTPS, guest and attacker denial, direct EHR bypass,
gateway forwarding, the nftables default-deny policy, Suricata runtime state,
EHR authentication/database behavior, and a Suricata alert generated by the
attack simulation. The exact commands and captured output are in
[docs/evidence.md](docs/evidence.md). DHCP/DNS is not included in that proof
because the gateway does not currently run dnsmasq.

## Portfolio evidence

For a project walkthrough, capture:

1. `make test` showing all policy tests passing.
2. `make attack` showing blocked internal probes.
3. Grafana's **ClinicGuard Security Overview** dashboard showing proxy and IDS
   log streams at
   <http://localhost:3000>.
4. The Mermaid topology in
   [docs/architecture.md](docs/architecture.md).

## Limitations

Docker networks simulate routed segmentation; they are not physical VLANs.
All data is synthetic. ClinicGuard is an educational security lab and is not
a HIPAA compliance certification or production healthcare network.
