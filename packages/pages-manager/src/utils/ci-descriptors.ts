import fs from 'node:fs'
import { DOCS_CI_PATH, join } from './paths'
import { extractPRNumber, getDisplayName, getReferenceType } from './reference-types'

export type CIDescriptor = {
  path: string
  displayName: string
  fullPath: string
  artifacts: string[]
  prNumber: number
  isPR: boolean
}

export const getCIDescriptors = (): {
  all: CIDescriptor[]
  main: CIDescriptor | null
  prs: CIDescriptor[]
  branches: CIDescriptor[]
} => {
  if (!fs.existsSync(DOCS_CI_PATH) || !fs.statSync(DOCS_CI_PATH).isDirectory()) {
    return { all: [], main: null, prs: [], branches: [] }
  }

  const entries = fs.readdirSync(DOCS_CI_PATH, { withFileTypes: true })

  const allDescriptors = entries
    .filter((entry) => entry.isDirectory())
    .map(({ name }) => {
      const fullPath = join(DOCS_CI_PATH, name)
      const subfolderEntries = fs.readdirSync(fullPath, { withFileTypes: true })

      const artifacts = subfolderEntries
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)

      const type = getReferenceType(name)
      const isPR = type === 'pr-and-branch'
      const prNumber = extractPRNumber(name).number
      const displayName = getDisplayName(name)

      return {
        path: name,
        displayName,
        fullPath,
        artifacts,
        prNumber,
        isPR
      }
    })

  const mainDescriptor = allDescriptors.find(({ path }) => path === 'main') ?? null

  const prDescriptors = allDescriptors
    .filter(({ isPR }) => isPR)
    .sort((a, b) => b.prNumber - a.prNumber)

  const branchDescriptors = allDescriptors.filter(({ isPR, path }) => !isPR && path !== 'main')

  return {
    all: allDescriptors,
    main: mainDescriptor,
    prs: prDescriptors,
    branches: branchDescriptors
  }
}
