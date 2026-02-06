import path from 'node:path'
import { fileURLToPath } from 'node:url'

export const getRootPath = (): string => {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  return path.resolve(__dirname, '../../../..')
}

export const join = (...segments: string[]): string => path.join(...segments)

export const DOCS_API_REFERENCE_PATH = join(getRootPath(), 'docs', 'api-reference')
export const ARTIFACTS_PATH = join(getRootPath(), 'artifacts')
export const API_REFERENCE_ARTIFACTS_PATH = join(ARTIFACTS_PATH, 'api-reference')
export const DOCS_CI_PATH = join(getRootPath(), 'docs', 'ci')
