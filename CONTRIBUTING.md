# Contributing to ClinicGuard

Use a feature branch and keep changes focused:

```bash
git switch -c feat/short-description
docker compose config
make test
make attack
git diff --check
```

Security-sensitive changes must include a regression test and update the
architecture or threat-model documentation. Do not add real patient data,
credentials, private keys, generated certificates, or unreviewed images.

Pull requests run Compose validation, policy tests, attack simulation, secret
scanning, Bandit, Trivy, and Hadolint.
