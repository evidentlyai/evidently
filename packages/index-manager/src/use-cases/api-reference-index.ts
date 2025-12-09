import fs from 'node:fs'

import { produceApiReferenceIndex } from '@lib/produce-indexes/api-reference-index'
import { getRootPath, join } from '@lib/utils'

const API_REFERENCE_ARTIFACTS_PATH = 'artifacts/api-reference'

const prepareApiReference = (): void => {
  const apiReferencePath = join(getRootPath(), API_REFERENCE_ARTIFACTS_PATH)

  // Check if the directory exists
  if (!fs.existsSync(apiReferencePath)) {
    console.log(`${API_REFERENCE_ARTIFACTS_PATH} folder does not exist`)
    return
  }

  // Check if it's actually a directory
  const stats = fs.statSync(apiReferencePath)
  if (!stats.isDirectory()) {
    console.log(`${API_REFERENCE_ARTIFACTS_PATH} is not a directory`)
    return
  }

  // Read directory contents
  const entries = fs.readdirSync(apiReferencePath, { withFileTypes: true })

  // Filter for folders only
  const folders = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name)

  if (folders.length === 0) {
    console.log('No folders found in artifacts/api-reference')
    return
  }

  // Copy folders to ./docs/api-reference

  const docsApiReferencePath = join(getRootPath(), 'docs', 'api-reference')

  // Create docs/api-reference directory if it doesn't exist
  if (!fs.existsSync(docsApiReferencePath)) {
    fs.mkdirSync(docsApiReferencePath, { recursive: true })
    console.log(`Created directory: ${docsApiReferencePath}`)
  }

  console.log('Copying folders to docs/api-reference:')
  for (const folder of folders) {
    const sourceFolderPath = join(apiReferencePath, folder)
    const destFolderPath = join(docsApiReferencePath, folder)

    // Copy folder recursively with force overwrite
    fs.cpSync(sourceFolderPath, destFolderPath, {
      recursive: true,
      force: true
    })

    console.log(`Copied: ${folder}`)
  }
}

const printApiReferenceIndex = (): void => {
  const result = produceApiReferenceIndex()

  console.log(result)
}

const writeApiReferenceIndex = (): void => {
  const apiReferencePath = join(getRootPath(), 'docs', 'api-reference')
  const apiReferencePathIndex = join(apiReferencePath, 'index.html')

  if (!fs.existsSync(apiReferencePath)) {
    fs.mkdirSync(apiReferencePath, { recursive: true })
    console.log(`Created directory: ${apiReferencePath}`)
  }

  const result = produceApiReferenceIndex()
  fs.writeFileSync(apiReferencePathIndex, result)
}

export const apiReferenceIndex = {
  prepareApiReference,
  printApiReferenceIndex,
  writeApiReferenceIndex
}
