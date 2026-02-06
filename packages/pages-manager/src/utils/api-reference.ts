import fs from 'node:fs'
import semver from 'semver'
import { DOCS_API_REFERENCE_PATH, join } from './paths'
import { extractPRNumber, getDisplayName, getReferenceType, trySemver } from './reference-types'

export type ApiReferenceDescriptor = {
  path: string
  displayName: string
  fullPath: string
  type: 'main' | 'unknown' | 'semver' | 'pr-and-branch'
  semver: string
  prNumber: number
}

export const getApiReferenceDescriptors = (): {
  all: ApiReferenceDescriptor[]
  main: ApiReferenceDescriptor | null
  others: ApiReferenceDescriptor[]
  semvers: ApiReferenceDescriptor[]
} => {
  if (
    !fs.existsSync(DOCS_API_REFERENCE_PATH) ||
    !fs.statSync(DOCS_API_REFERENCE_PATH).isDirectory()
  ) {
    return { all: [], main: null, others: [], semvers: [] }
  }

  const entries = fs.readdirSync(DOCS_API_REFERENCE_PATH, { withFileTypes: true })

  const allEntries = entries
    .filter((entry) => entry.isDirectory())
    .map(({ name }) => {
      const fullPath = join(DOCS_API_REFERENCE_PATH, name)
      const displayName = getDisplayName(name)
      const type = getReferenceType(name)

      return {
        path: name,
        displayName,
        type,
        fullPath,
        semver: trySemver(name),
        prNumber: extractPRNumber(name).number
      } as const
    })

  const mainDescriptor = allEntries.find(({ type }) => type === 'main') ?? null

  const prAndBranchDescriptors = allEntries
    .filter(({ type }) => type === 'pr-and-branch')
    .sort((a, b) => b.prNumber - a.prNumber)

  const unknownDescriptors = allEntries.filter(({ type }) => type === 'unknown')

  const semverDescriptors = allEntries
    .filter(({ type }) => type === 'semver')
    .sort((a, b) => -semver.compare(a.semver, b.semver))

  return {
    main: mainDescriptor,
    others: [...prAndBranchDescriptors, ...unknownDescriptors],
    semvers: semverDescriptors,
    all: allEntries
  }
}
