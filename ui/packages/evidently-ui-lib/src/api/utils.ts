import type { ErrorData, OptionalID, StrictID } from '~/api/types/utils'

export const ensureID: <Entity extends OptionalID>(e: Entity) => StrictID<Entity> = (e) => {
  if (e.id) {
    return { ...e, id: e.id }
  }

  throw `"id" is missing in object: ${JSON.stringify(e)}`
}

export const ensureIDInArray: <Entity extends OptionalID>(e: Entity[]) => StrictID<Entity>[] = (
  e
) => {
  return e.map(ensureID)
}

export const expectJsonRequest = (request: Request) => {
  if (request.headers.get('Content-type') !== 'application/json') {
    throw new Response('Unsupported Media Type', { status: 415 })
  }
}

export const isSuccessData = <T>(e: T): e is Exclude<T, ErrorData> =>
  !e || typeof e !== 'object' || !('error' in e)
