import semver from 'semver'

const checkIsPRAndBranch = (name: string) => name.startsWith('pr-')
export const trySemver = (name: string) => semver.clean(name) ?? ''

export const getReferenceType = (name: string) => {
  if (name === 'main') {
    return 'main'
  }

  if (trySemver(name)) {
    return 'semver'
  }

  if (checkIsPRAndBranch(name)) {
    return 'pr-and-branch'
  }

  return 'unknown'
}

export const extractPRNumber = (name: string) => {
  const type = getReferenceType(name)

  if (type !== 'pr-and-branch') {
    return { number: 0, rest: name }
  }

  const [_, number, ...rest] = name.split('-')

  return { number: Number.parseInt(number), rest: rest.join('-') }
}

export const getDisplayName = (name: string) => {
  const type = getReferenceType(name)

  if (type === 'pr-and-branch') {
    const { number, rest } = extractPRNumber(name)
    return `PR ${number} (${rest})`
  }

  return name
}
