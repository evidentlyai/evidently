import { execSync } from 'node:child_process'
import { getRootPath } from './paths'

type FolderLastModificationTimestamp = {
  lastModificationTimestamp: number
  lastModificationDateString: string
}

export const getFolderLastModificationTimestamp = (
  folderPath: string
): FolderLastModificationTimestamp | null => {
  const gitOptions = { encoding: 'utf-8', stdio: 'pipe' } as const

  try {
    const output = execSync(
      `git -C "${getRootPath()}" log -1 --format=%ct -- "${folderPath}"`,
      gitOptions
    ).trim()

    if (!output) return null

    const commitTime = Number.parseInt(output, 10)
    if (Number.isNaN(commitTime)) return null

    const lastModificationTimestamp = commitTime * 1000
    const lastModificationDateString = new Date(lastModificationTimestamp).toString()

    return { lastModificationTimestamp, lastModificationDateString }
  } catch {
    console.error(`Error getting last modification timestamp for ${folderPath}`)
    return null
  }
}
