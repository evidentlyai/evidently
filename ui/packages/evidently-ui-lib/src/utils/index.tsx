export function formatDate(date: Date): string {
  return (
    `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}` +
    `-${date.getDate().toString().padStart(2, '0')}` +
    `T${date.getHours().toString().padStart(2, '0')}:${date
      .getMinutes()
      .toString()
      .padStart(2, '0')}`
  )
}

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
