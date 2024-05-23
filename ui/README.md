# Evidently UI

We have two UI projects:

- [service](service) - monitoring UI
- [standalone](standalone) - additional package we use for embedding graphics for instance in jupyter notebook and other places

## Requirements

- [node.js](https://nodejs.org/en/download) (v20 or higher)
- we also use [pnpm](https://pnpm.io/installation) (v9) as package manager

## Install dependencies

```shell
pnpm install
```

## Run Service

For now you have to have [evidently ui](https://docs.evidentlyai.com/user-guide/monitoring/monitoring_ui) (as a backend) running on `localhost:8000`

```shell
# inside service folder
pnpm dev
```

## Build Service

```shell
# inside service folder
pnpm build
```

```shell
litestar --app evidently.ui.cli_app:create_app schema openapi --output my-specs.yml && npx openapi-typescript ./my-specs.yml -o ./ui/packages/evidently-ui-lib/src/api/types/schema.d.ts
```
