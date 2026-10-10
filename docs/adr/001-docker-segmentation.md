# ADR 001: Simulate routed trust zones with Docker networks

## Context

ClinicGuard needs distinct staff, guest, server, management, and attacker
zones whose traffic can be inspected and controlled. The lab must run on a
laptop and remain reproducible from source.

## Decision

Use one Docker bridge network per trust zone and connect a dedicated Linux
gateway to each network. Mark the networks `internal: true` so the gateway is
the intentional routing point. Implement forwarding policy with nftables.

## Alternatives considered

- Use Docker's default networking: rejected because it hides the routing
  topology and makes the security policy difficult to inspect and test.
- Build the lab on physical VLANs: deferred because it requires additional
  hardware and is less portable for a laptop-based project.
- Use a full virtualized firewall appliance: deferred because it adds
  operational complexity before the core learning goals are complete.

## Consequences

The topology is portable, version-controlled, and suitable for automated
tests. Docker networks are a simulation of segmentation, not physical
802.1Q VLANs. The gateway needs elevated Linux networking capabilities, and
the network behavior must be validated explicitly because Docker remains an
abstraction over the host network.

