import fs from 'node:fs'

import { produceApiReferenceIndex } from '@lib/produce-indexes/api-reference-index'
import {
  API_REFERENCE_ARTIFACTS_PATH,
  DOCS_API_REFERENCE_PATH,
  consoleGroup,
  consoleGroupEnd,
  getApiReferenceDescriptors,
  getFolderLastModificationTimestamp,
  join
} from '@lib/utils'

const copyNewApiReferences = (): void => {
  if (!fs.existsSync(API_REFERENCE_ARTIFACTS_PATH)) {
    console.log(`${API_REFERENCE_ARTIFACTS_PATH} folder does not exist`)
    return
  }

  const stats = fs.statSync(API_REFERENCE_ARTIFACTS_PATH)
  if (!stats.isDirectory()) {
    console.log(`${API_REFERENCE_ARTIFACTS_PATH} is not a directory`)
    return
  }

  const entries = fs.readdirSync(API_REFERENCE_ARTIFACTS_PATH, { withFileTypes: true })

  const folders = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name)

  if (folders.length === 0) {
    console.log(`No folders found in ${API_REFERENCE_ARTIFACTS_PATH}`)
    return
  }

  if (!fs.existsSync(DOCS_API_REFERENCE_PATH)) {
    fs.mkdirSync(DOCS_API_REFERENCE_PATH, { recursive: true })
    console.log(`Created directory: ${DOCS_API_REFERENCE_PATH}`)
  }

  console.log(`Copying folders to ${DOCS_API_REFERENCE_PATH}:`)
  for (const folder of folders) {
    const sourceFolderPath = join(API_REFERENCE_ARTIFACTS_PATH, folder)
    const destFolderPath = join(DOCS_API_REFERENCE_PATH, folder)

    if (fs.existsSync(destFolderPath)) {
      fs.rmSync(destFolderPath, { recursive: true, force: true })
    }

    fs.cpSync(sourceFolderPath, destFolderPath, {
      recursive: true
    })

    console.log(`Copied: ${folder}`)
  }
}

const printApiReferenceIndex = (): void => {
  const result = produceApiReferenceIndex()

  console.log(result)
}

const writeApiReferenceIndex = (): void => {
  const apiReferencePathIndex = join(DOCS_API_REFERENCE_PATH, 'index.html')

  if (!fs.existsSync(DOCS_API_REFERENCE_PATH)) {
    fs.mkdirSync(DOCS_API_REFERENCE_PATH, { recursive: true })
    console.log(`Created directory: ${DOCS_API_REFERENCE_PATH}`)
  }

  const result = produceApiReferenceIndex()
  fs.writeFileSync(apiReferencePathIndex, result)
}

const deleteOldBranchFolders = (): void => {
  consoleGroup('Checking for old api-references to delete')
  consoleGroupEnd()
  const { others } = getApiReferenceDescriptors()

  const TWO_WEEKS_AGO = Date.now() - 14 * 24 * 60 * 60 * 1000
  let deletedCount = 0

  for (const otherApiRef of others) {
    const folderLastModTimestamp = getFolderLastModificationTimestamp(otherApiRef.fullPath)

    if (!folderLastModTimestamp) {
      console.log(`No last modification timestamp found for ${otherApiRef.path}`)
      continue
    }

    consoleGroup(otherApiRef.path)
    console.log(`Last modification: ${folderLastModTimestamp.lastModificationDateString}`)

    if (folderLastModTimestamp.lastModificationTimestamp <= TWO_WEEKS_AGO) {
      fs.rmSync(otherApiRef.fullPath, { recursive: true, force: true })
      console.log(`Deleted: ${otherApiRef.path}`)
      deletedCount++
    }

    consoleGroupEnd()
  }

  if (deletedCount === 0) {
    consoleGroup('No old branch folders to delete')
    consoleGroupEnd()
  }
}

export const apiReferenceIndex = {
  copyNewApiReferences,
  printApiReferenceIndex,
  writeApiReferenceIndex,
  deleteOldBranchFolders
}
