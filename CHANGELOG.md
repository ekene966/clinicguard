# Changelog

## [Unreleased]

Future work is organized in the staged roadmap in the README.

## [0.2.0] - 2026-10-10

### Added

- Health checks for the gateway and EHR proxy.
- HTTP security headers on both TLS proxy boundaries.
- `.env.example` for local configuration guidance.
- Gitleaks secret scanning and Bandit Python security linting in CI.

### Validation

- Compose configuration validation passes.
- Existing policy integration tests pass.
- Attack simulation remains part of CI.

## [0.1.0] - 2026-10-10

### Added

- Docker trust-zone segmentation and gateway default-deny firewalling.
- TLS-protected synthetic EHR access.
- Suricata IDS monitoring.
- Loki, Promtail, and Grafana observability.
- Automated policy tests, attack simulation, and GitHub Pages documentation.
