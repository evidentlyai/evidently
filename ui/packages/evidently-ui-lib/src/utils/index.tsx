import { LoaderFunctionArgs, ActionFunction } from 'react-router-dom'

interface DataManipulation<LoaderData> {
  loader: (args: LoaderFunctionArgs) => Promise<LoaderData>
  action: ActionFunction
}

export type GetLoaderAction<Provider, LoaderData> = ({
  api
}: {
  api: Provider
}) => Partial<DataManipulation<LoaderData>>

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
