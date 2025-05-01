// https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html
export function assertNever(x: never): never {
  throw `Unexpected object: ${x}`
}

export function assertNeverActionVariant(x: never): never {
  throw `Unexpected action variant: ${x}`
}

export const REST_PARAMS_FOR_FETCHER_SUBMIT = {
  method: 'post',
  encType: 'application/json'
} as const

export const clamp = ({ value, min, max }: Record<'value' | 'min' | 'max', number>) =>
  Math.min(Math.max(value, min), max)
