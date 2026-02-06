import fs from 'node:fs'

import { produceCIIndex } from '@lib/produce-pages/ci-page'
import { CI_ARTIFACTS } from '@lib/utils/ci-artifacts'
import { ARTIFACTS_PATH, DOCS_CI_PATH, join } from '@lib/utils/paths'

const copyNewCIArtifacts = (): void => {
  if (!fs.existsSync(ARTIFACTS_PATH)) {
    console.log(`${ARTIFACTS_PATH} folder does not exist`)
    return
  }

  const stats = fs.statSync(ARTIFACTS_PATH)
  if (!stats.isDirectory()) {
    console.log(`${ARTIFACTS_PATH} is not a directory`)
    return
  }

  if (!fs.existsSync(DOCS_CI_PATH)) {
    fs.mkdirSync(DOCS_CI_PATH, { recursive: true })
    console.log(`Created directory: ${DOCS_CI_PATH}`)
  }

  console.log(`Copying CI artifacts to ${DOCS_CI_PATH}:`)
  for (const ci_artifact of CI_ARTIFACTS) {
    const sourcePath = join(ARTIFACTS_PATH, ci_artifact)
    if (!fs.existsSync(sourcePath)) continue

    const stats = fs.statSync(sourcePath)
    if (!stats.isDirectory()) continue

    const entries = fs.readdirSync(sourcePath, { withFileTypes: true })

    for (const entry of entries) {
      if (!entry.isDirectory()) continue
      const destDir = join(DOCS_CI_PATH, entry.name, ci_artifact)
      if (fs.existsSync(destDir)) {
        fs.rmSync(destDir, { recursive: true, force: true })
      }
      const sourceEntryPath = join(sourcePath, entry.name)
      fs.cpSync(sourceEntryPath, destDir, { recursive: true })
      console.log(`Copied: ${entry.name}/${ci_artifact}`)
    }
  }
}

const printCIIndex = (): void => {
  const result = produceCIIndex()

  console.log(result)
}

const writeCIndex = (): void => {
  const ciIndexPath = join(DOCS_CI_PATH, 'index.html')

  if (!fs.existsSync(DOCS_CI_PATH)) {
    fs.mkdirSync(DOCS_CI_PATH, { recursive: true })
    console.log(`Created directory: ${DOCS_CI_PATH}`)
  }

  const result = produceCIIndex()
  fs.writeFileSync(ciIndexPath, result)
}

export const ci = {
  copyNewCIArtifacts,
  printCIIndex,
  writeCIndex
}
