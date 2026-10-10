# ClinicGuard architecture

ClinicGuard models five trust zones connected through a Linux gateway:

```mermaid
flowchart LR
    A[Attacker<br/>10.10.66.0/24] --> G[Gateway / nftables<br/>.254 on each zone]
    S[Staff<br/>10.10.10.0/24] --> G
    U[Guest Wi-Fi<br/>10.10.20.0/24] --> G
    G --> E[Server zone<br/>10.10.30.0/24]
    G --> M[Management<br/>10.10.99.0/24]
```

The gateway is the intended routing and enforcement point. Each Docker network
is marked `internal: true` so the lab does not accidentally provide a direct
external path that bypasses the gateway.

## Initial access policy

| Source | Destination | Policy |
| --- | --- | --- |
| Staff | EHR | Allow TCP 443 only |
| Staff | Internet/DNS | Allow DNS, HTTP, HTTPS |
| Guest | Internet/DNS | Allow DNS, HTTP, HTTPS |
| Guest | Staff, server, management | Deny |
| Attacker | Internal zones | Deny and alert |
| Management | All zones | Read-only monitoring access |

The policy will be implemented and tested in later phases. This document
describes the intended behavior, not a claim that the Phase 1 scaffold already
enforces it.

