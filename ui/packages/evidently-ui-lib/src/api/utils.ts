import type { ActionFunction, LoaderFunctionArgs } from 'react-router-dom'
import type { OptionalID, StrictID } from '~/api/types/utils'

export type ILoaderAction<LoaderData> = {
  loader: (args: LoaderFunctionArgs) => Promise<LoaderData>
  action: ActionFunction
}

export type GetLoaderAction<Provider, LoaderData> = ({
  api
}: {
  api: Provider
}) => Partial<ILoaderAction<LoaderData>>

export const ensureID: <Entity extends OptionalID>(e: Entity) => StrictID<Entity> = (e) => {
  if (e.id) {
    return { ...e, id: e.id }
  }

  throw `"id" is missing in object: ${JSON.stringify(e)}`
}

export const expectJsonRequest = (request: Request) => {
  if (request.headers.get('Content-type') !== 'application/json') {
    throw new Response('Unsupported Media Type', { status: 415 })
  }
}
