import fs from 'node:fs'

import { produceApiReferenceIndex } from '@lib/produce-indexes/api-reference-index'
import {
  API_REFERENCE_ARTIFACTS_PATH,
  DOCS_API_REFERENCE_PATH,
  colorize,
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

    fs.cpSync(sourceFolderPath, destFolderPath, { recursive: true })

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
  console.log(colorize.branch('Checking for old api-references to delete'))
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
    const timeSpentMs = Date.now() - folderLastModTimestamp.lastModificationTimestamp
    const timeSpentDays = Number.parseFloat((timeSpentMs / (1000 * 60 * 60 * 24)).toFixed(2))

    const willDelete = folderLastModTimestamp.lastModificationTimestamp <= TWO_WEEKS_AGO

    console.log(
      `${colorize.time('Time since last modification:')} ${colorize.age(timeSpentDays)} ${colorize.time('days ago')}`
    )
    console.log(
      `${colorize.date('Last modification:')} ${colorize.date(folderLastModTimestamp.lastModificationDateString)}`
    )

    if (willDelete) {
      fs.rmSync(otherApiRef.fullPath, { recursive: true, force: true })
      console.log(colorize.deleted(`Deleted: ${otherApiRef.path}`))
      deletedCount++
    } else {
      console.log(colorize.kept('Kept (less than 2 weeks old)'))
    }

    consoleGroupEnd()
  }

  if (deletedCount === 0) {
    console.log(colorize.branch('No old branch folders to delete'))
    console.log(colorize.kept('All branch folders are recent'))
  } else {
    console.log(
      colorize.branch(
        `Successfully deleted ${deletedCount} old branch folder${deletedCount === 1 ? '' : 's'}`
      )
    )
  }
}

export const apiReferenceIndex = {
  copyNewApiReferences,
  printApiReferenceIndex,
  writeApiReferenceIndex,
  deleteOldBranchFolders
}
