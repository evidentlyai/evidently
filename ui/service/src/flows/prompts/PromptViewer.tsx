import type { PromptTemplate } from 'evidently-ui-lib/api/types'
import { CollapsiblePromptDisplay } from 'evidently-ui-lib/components/Prompts/CollapsiblePromptDisplay'
import { useState } from 'react'

type PromptViewerProps = {
  data: PromptTemplate
  buttonTitle?: string
}

export const PromptViewer = (props: PromptViewerProps) => {
  const { /*data,*/ buttonTitle } = props

  // const promptFetcher = useLoader('/api/prompt-preview')

  const [details, setDetails] = useState(false)

  // const prompt = promptFetcher.data
  //   ? typeof promptFetcher.data === 'string'
  //     ? promptFetcher.data
  //     : promptFetcher.data && `Error: ${promptFetcher.data.error.detail}`
  //   : ''

  // // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  // useEffect(() => {
  //   if (promptFetcher.state === 'idle' && details) {
  //     promptFetcher.load({
  //       query: { payload: JSON.stringify({ template: data } satisfies PromptTemplateRequestModel) }
  //     })
  //   }
  // }, [
  //   details,
  //   // may be track manually better?

  //   // template.include_category,
  //   // template.criteria,
  //   // template.include_score,
  //   // template.include_reasoning
  //   JSON.stringify(data)
  // ])

  // const isLoading = promptFetcher.state !== 'idle'

  //   <CollapsiblePromptDisplay
  //   details={details}
  //   setDetails={setDetails}
  //   buttonTitle={buttonTitle}
  //   prompt={prompt}
  //   isLoading={isLoading}
  // />

  return (
    <CollapsiblePromptDisplay
      details={details}
      setDetails={setDetails}
      buttonTitle={buttonTitle}
      prompt={''} // TODO: fix
      isLoading={false} // TODO: fix
    />
  )
}
