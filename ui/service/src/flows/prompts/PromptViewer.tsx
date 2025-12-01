import type { PromptTemplate } from 'evidently-ui-lib/api/types'
import { CollapsiblePromptDisplay } from 'evidently-ui-lib/components/Prompts/CollapsiblePromptDisplay'
import { useEffect, useState } from 'react'
import { useLoader } from '~/routes/type-safe-route-helpers/hooks'

type PromptViewerProps = {
  data: PromptTemplate
  buttonTitle?: string
}

export const PromptViewer = (props: PromptViewerProps) => {
  const { data, buttonTitle } = props

  const promptFetcher = useLoader('/api/load-prompt-preview')

  const [details, setDetails] = useState(false)

  const prompt = promptFetcher.data
    ? typeof promptFetcher.data === 'string'
      ? promptFetcher.data
      : promptFetcher.data && `Error: ${promptFetcher.data.error.detail}`
    : ''

  const payload = JSON.stringify(data satisfies PromptTemplate)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (!(details && promptFetcher.state === 'idle')) {
      return
    }

    promptFetcher.load({ query: { payload } })
  }, [details, payload])

  const isLoading = promptFetcher.state !== 'idle'

  return (
    <CollapsiblePromptDisplay
      details={details}
      setDetails={setDetails}
      buttonTitle={buttonTitle}
      prompt={prompt}
      isLoading={isLoading}
    />
  )
}
