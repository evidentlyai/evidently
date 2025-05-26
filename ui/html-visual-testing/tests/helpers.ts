import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

export const HELPERS = {
  getDirname: () => {
    const __filename = fileURLToPath(import.meta.url)
    const __dirname = path.dirname(__filename)
    return { __dirname }
  },
  getConfigPath: () => path.join(HELPERS.getDirname().__dirname, '..', './config.json'),
  readConfig: () => JSON.parse(fs.readFileSync(HELPERS.getConfigPath())) as Record<string, string[]>
}
