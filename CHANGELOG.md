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

## [0.4.0] - 2026-10-10

### Added

- Health checks and a memory limit for core observability services.
- Synthetic EHR, Loki, and Grafana backup helper.
- Production-style deployment and restore guidance.

## [1.0.0] - 2026-10-10

### Added

- Trivy filesystem/IaC scanning and Hadolint Dockerfile linting.
- Dependabot configuration for GitHub Actions.
- Pull request, contributing, and security policy guidance.
