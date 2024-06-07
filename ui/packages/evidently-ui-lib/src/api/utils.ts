import type { OptionalID, StrictID } from '~/api/types/utils'

export const ensureID: <Entity extends OptionalID>(e: Entity) => StrictID<Entity> = (e) => {
  if (e.id) {
    return { ...e, id: e.id }
  }

  throw `"id" is missing on object: ${JSON.stringify(e)}`
}
