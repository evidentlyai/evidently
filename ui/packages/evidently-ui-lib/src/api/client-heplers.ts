import createClient from 'openapi-fetch'
import { json } from 'react-router-dom'
import type { ErrorData, ErrorResponse } from '~/api/types/utils'

import { BackendPaths } from '~/api/types'

export type API_CLIENT_TYPE = ReturnType<typeof createClient<BackendPaths>>

type ClientGenericResponse<D = any> =
  | {
      data: D
      error?: never
      response: Response
    }
  | {
      data?: never
      error: ErrorResponse
      response: Response
    }

type ResponseParserArgs = { notThrowExc: boolean }

type DetermineReturnType<T extends ResponseParserArgs> = T extends {
  notThrowExc: true
}
  ? typeof returnErrorIfResponseNotOk
  : T extends { notThrowExc: false }
  ? typeof throwErrorIfResponseNotOk
  : T extends {}
  ? typeof throwErrorIfResponseNotOk
  : never

export function responseParser<T extends ResponseParserArgs>(args?: T): DetermineReturnType<T> {
  if (args?.notThrowExc) {
    return returnErrorIfResponseNotOk as DetermineReturnType<T>
  }

  return throwErrorIfResponseNotOk as DetermineReturnType<T>
}

const throwErrorIfResponseNotOk = <R extends ClientGenericResponse>(
  genResponse: R
): NonNullable<R['data']> => {
  const { data, error, response } = genResponse
  if (error) {
    throw json(error, { status: response.status })
  }

  return data
}

const returnErrorIfResponseNotOk = <R extends ClientGenericResponse>(
  genResponse: R
): NonNullable<R['data']> | ErrorData => {
  const { data, error, response } = genResponse

  if (error) {
    return { error: { ...error, status_code: response.status } }
  }

  return data
}
