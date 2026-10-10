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

5. Start the scaffold:

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

The gateway uses a default-deny forwarding policy. Staff can reach the EHR
reverse proxy over HTTPS on TCP 443; guest and attacker clients must not reach
the server zone. The lab certificate is self-signed and intended for testing,
so validation commands use `curl -k`.

To verify the proxy from inside the server zone:

```bash
docker compose exec gateway wget --no-check-certificate -qO- https://10.10.30.10/
```

The response should be served by the synthetic backend through nginx. Client
to server policy tests will be added with the integration test harness once
the Docker Desktop routed-network behavior is covered.

## Troubleshooting

- If Docker commands fail inside WSL, confirm Docker Desktop is running and
  that WSL integration is enabled for the active distribution.
- Prefer `~/src/clinicguard` over `/mnt/c/...` for reliable Linux permissions
  and bind mounts.
- The gateway requires Linux networking capabilities. Docker Desktop may
  display a warning when those capabilities are unavailable; do not weaken the
  policy to hide that warning.
