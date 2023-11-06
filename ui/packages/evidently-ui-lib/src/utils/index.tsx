import { LoaderFunctionArgs, ActionFunction } from 'react-router-dom'
import type { Api } from '~/api'

interface DataManipulation<loaderData> {
  loader: (args: LoaderFunctionArgs) => Promise<loaderData>
  action: ActionFunction
}

export type InJectAPI<T> = ({ api }: { api: Api }) => Partial<DataManipulation<T>>

export const expectJsonRequest = (request: Request) => {
  if (request.headers.get('Content-type') !== 'application/json') {
    throw new Response('Unsupported Media Type', { status: 415 })
  }
}

export function formatDate(date: any): string {
  if (typeof date !== typeof new Date()) {
    console.log(`not a date ${typeof date}: ${date}`)
    return date
  }
  return (
    `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}` +
    `-${date.getDate().toString().padStart(2, '0')}` +
    `T${date.getHours().toString().padStart(2, '0')}:${date
      .getMinutes()
      .toString()
      .padStart(2, '0')}`
  )
}
