# ClinicGuard

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

The observability stack includes Loki, Promtail, and Grafana. Run
`make attack` to exercise blocked HTTPS probes and inspect the resulting logs.
See the [threat model](docs/threat-model.md) and
[HIPAA alignment map](docs/hipaa-control-map.md) for scope and limitations.

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

## Expected proof

```text
Staff HTTPS to the gateway       PASS
Guest HTTPS to the gateway       BLOCKED
Attacker HTTPS to the gateway    BLOCKED
Staff direct EHR bypass          BLOCKED
Forwarding enabled               PASS
Forward chain policy             DROP
```

Run `make test` to verify these assertions. Run `make attack` to produce
blocked-probe evidence. The test suite runs requests from the individual
client containers so it cannot accidentally bypass the gateway with a
multi-homed test container.

## Portfolio evidence

For a project walkthrough, capture:

1. `make test` showing all policy tests passing.
2. `make attack` showing blocked internal probes.
3. Grafana's **ClinicGuard Security Overview** dashboard at
   <http://localhost:3000>.
4. The Mermaid topology in
   [docs/architecture.md](docs/architecture.md).

## Limitations

Docker networks simulate routed segmentation; they are not physical VLANs.
All data is synthetic. ClinicGuard is an educational security lab and is not
a HIPAA compliance certification or production healthcare network.
