# Validation evidence

This file records the shape of the reproducible evidence used for the
portfolio claims. Run the commands from the repository root with Docker
running:

```text
$ make test
..........                                                               [100%]
10 passed

$ make attack
ClinicGuard attack simulation
BLOCKED 10.10.10.254:443
BLOCKED 10.10.20.254:443
BLOCKED 10.10.30.10:443
BLOCKED 10.10.99.254:443
```

The live CI equivalents are the [policy workflow](https://github.com/ekene966/clinicguard/actions/workflows/ci.yml)
and [security workflow](https://github.com/ekene966/clinicguard/actions/workflows/security.yml).
The policy tests run the attacker simulation and verify a matching Suricata
alert in `eve.json`; they also verify the EHR unit tests, network policy, and
runtime Suricata state.

For visual evidence, start the stack with `make up`, open
<http://localhost:3000>, and select **ClinicGuard Security Overview**. The
dashboard should show `service_name=suricata`, `service_name=gateway-nginx`,
and `service_name=ehr-nginx` streams after `make attack`.
