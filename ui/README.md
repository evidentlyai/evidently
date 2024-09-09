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


## Code quality

We use `biome` to lint, format and sort imports

### vscode
We recommend to use [biome vscode](https://biomejs.dev/reference/vscode) plugin.

`.vscode/settings.json` is following:
```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "editor.formatOnSave": true,
  "biome.lspBin": "./ui/node_modules/@biomejs/biome/bin/biome",
  "biome.searchInPath": false,
  "editor.codeActionsOnSave":{
    "source.organizeImports.biome": "explicit"
  }
}
```

### I like to use the terminal. Just show me the cli

```bash
# in `ui` folder
pnpm code-check          # just check: format, sort imports and lint
pnpm code-check --fix  # check and apply appropriate diff (where possible)
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
