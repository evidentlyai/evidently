import { type API, responseParser } from '~/api/client-heplers'

export const getVersion = ({ api }: API) => api.GET('/api/version').then(responseParser())
