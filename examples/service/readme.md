# Evidently Service Examples

## Using remote workspace

1. Start Evidently Service in docker container

```bash
sh run_service.sh
```

2. Use `RemoteWorkspace` to add projects and snapshots to your service. For example, run 

```bash
python remote_demo_project.py
```

It will populate your service with demo project and print it's id.