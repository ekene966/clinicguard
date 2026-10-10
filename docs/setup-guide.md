# Setup guide: Windows + WSL2

1. Install Docker Desktop and enable **Use the WSL 2 based engine**.
2. In Docker Desktop, enable WSL integration for the distribution you use.
3. Open that distribution and keep the repository inside its Linux filesystem:

   ```bash
   mkdir -p ~/src
   cd ~/src
   git clone <repository-url> clinicguard
   cd clinicguard
   ```

4. Verify the toolchain:

   ```bash
   docker --version
   docker compose version
   git --version
   ```

5. Start the stack:

   ```bash
   docker compose config
   docker compose up -d --build
   docker compose ps
   ```

To inspect the foundation routes:

```bash
docker compose exec staff-client ip route
docker compose exec guest-client ip route
docker compose exec gateway cat /proc/sys/net/ipv4/ip_forward
```

Docker Desktop may expose the forwarding sysctl as read-only inside the
container. The Compose-level sysctl is the authoritative configuration; the
entrypoint does not attempt to rewrite it at runtime.

The gateway uses a default-deny policy. Staff reach the gateway's EHR reverse
proxy over HTTPS on TCP 443; guest and attacker clients cannot use that
listener. The lab certificate is self-signed and intended for testing, so
validation commands use `curl -k`.

To verify the proxy from inside the server zone:

```bash
docker compose exec gateway wget --no-check-certificate -qO- https://10.10.30.10/
```

The response should be served by the synthetic backend through the EHR nginx
proxy. From a staff client, test the policy boundary with:

```bash
docker compose exec staff-client wget --no-check-certificate -qO- https://10.10.10.254/
```

The same request from the guest gateway address (`10.10.20.254`) or attacker
gateway address (`10.10.66.254`) should time out. The zone networks remain
`internal: true`; do not remove that setting to make cross-bridge traffic
appear to work, because Docker would then provide a host-level bypass around
the gateway policy.

Run the automated policy checks from the repository root:

```bash
make test
```

On Windows PowerShell, the Makefile selects `py -3.12`; on WSL/Linux it
selects `python3`. You can also run the suite directly with
`py -3.12 -m pytest -q` on Windows.

The tests execute each request from its own client container. This is
intentional: a test container attached to every zone would bypass the gateway
and produce a false result.

## Observability

Start the monitoring services with the rest of the stack:

```bash
docker compose up -d loki promtail grafana
```

Open Grafana at <http://localhost:3000>. The provisioned dashboard is
**ClinicGuard Security Overview** and uses Loki as its default data source.
The lab does not configure an administrator password or expose Grafana beyond
localhost; set `GF_SECURITY_ADMIN_PASSWORD` before using this stack outside a
local lab.

Logs are shared through named volumes rather than Docker Desktop's host log
path. Promtail collects Suricata `eve.json` and nginx access/error logs, and
ships them to Loki.

## Troubleshooting

- If Docker commands fail inside WSL, confirm Docker Desktop is running and
  that WSL integration is enabled for the active distribution.
- Prefer `~/src/clinicguard` over `/mnt/c/...` for reliable Linux permissions
  and bind mounts.
- The gateway requires Linux networking capabilities. Docker Desktop may
  display a warning when those capabilities are unavailable; do not weaken the
  policy to hide that warning.
