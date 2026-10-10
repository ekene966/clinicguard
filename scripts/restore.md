# Backup and restore

The local backup script captures the synthetic EHR SQLite database, Loki data,
and Grafana state:

```bash
make backup
```

To restore, stop the stack, copy the saved directories back into the named
volumes with a temporary helper container, and start the stack again. Never
restore untrusted files into a production host. The backup contains synthetic
data only, but it may include security logs and dashboard state.
