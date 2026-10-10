# ADR 002: Keep Docker Desktop internal networks and proxy at the gateway

## Context

On Docker Desktop's Linux engine, traffic between separate Docker bridge
networks marked `internal: true` can be blocked before it reaches a container
router. Removing `internal: true` makes the traffic appear to work, but lets
Docker provide a host-level bridge path that bypasses the intended gateway
policy.

## Decision

Keep every clinic trust-zone network internal. Terminate staff HTTPS on the
gateway's staff-zone address and proxy from the gateway to the EHR through its
server-zone interface. The gateway remains the policy and audit boundary.

## Alternatives considered

- Remove `internal: true`: rejected because it undermines the segmentation
  claim and allows a routing bypass.
- Attach every client directly to the server network: rejected because it
  defeats zone isolation.
- Depend on host-specific Docker firewall behavior: rejected because it is
  difficult to reproduce and test across Docker Desktop and Linux engines.

## Consequences

The lab has a reliable application-layer path on Docker Desktop while
preserving internal network boundaries. The gateway performs an additional
TLS proxy hop, and the design should be revalidated on native Linux if the
lab is later deployed outside Docker Desktop.
