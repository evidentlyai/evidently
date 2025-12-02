import { clientAPI } from 'api'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { PromptTemplate } from 'evidently-ui-lib/api/types'
import type { loadDataArgs } from 'evidently-ui-lib/router-utils/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/api/load-prompt-preview'

const crumb = { title: 'Load Prompt' }

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = ({ query }: loadDataArgs<{ queryKeys: 'payload' }>) => {
  const data = query.payload ?? ''
  const template = JSON.parse(data) as PromptTemplate

  return clientAPI
    .POST('/api/llm_judges/prompt_template', { body: { template }, parseAs: 'text' })
    .then(responseParser({ notThrowExc: true }))
}
