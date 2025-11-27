import {
  ExpandLessSharp as ExpandLessSharpIcon,
  ExpandMoreSharp as ExpandMoreSharpIcon
} from '@mui/icons-material'
import { Chip, Stack, Typography } from '@mui/material'
import { useState } from 'react'
import type { LLMPromptTemplateModel, PromptTemplate } from '~/api/types'

type BinaryTemplate = Extract<
  PromptTemplate,
  { type?: 'evidently:prompt_template:BinaryClassificationPromptTemplate' | null }
>

type BinaryTemplateSelectorProps = {
  prompts: LLMPromptTemplateModel[]
  onChangeBinaryTemplate: (template: BinaryTemplate, name: string) => void
}

export const BinaryTemplateSelector = (props: BinaryTemplateSelectorProps) => {
  const { prompts, onChangeBinaryTemplate } = props

  const [showMoreTemplates, setShowMoreTemplates] = useState(false)

  return (
    <Stack>
      <Typography variant='h6'>Binary classification templates</Typography>

      <Typography variant='body2' color='text.secondary' gutterBottom>
        Select one of our pre-defined templates to get started quickly.
      </Typography>

      <Stack mt={0.5} direction={'row'} gap={1} maxWidth={450} flexWrap={'wrap'}>
        {prompts
          .sort((a, b) => {
            const matters = ['PII', 'Negativity', 'Toxicity']
            return matters.includes(a.name) && !matters.includes(b.name) ? -1 : 1
          })
          .slice(0, showMoreTemplates ? prompts.length : 3)
          .map((prompt) => (
            <Chip
              key={prompt.name}
              label={prompt.name}
              variant={'outlined'}
              onClick={() => onChangeBinaryTemplate(prompt.template, `${prompt.name} LLM Judge`)}
            />
          ))}

        {!showMoreTemplates ? (
          <Chip
            label={'Show more'}
            variant={'filled'}
            icon={<ExpandMoreSharpIcon />}
            onClick={() => setShowMoreTemplates(true)}
          />
        ) : (
          <Chip
            label={'Hide'}
            variant={'filled'}
            icon={<ExpandLessSharpIcon />}
            onClick={() => setShowMoreTemplates(false)}
          />
        )}
      </Stack>
    </Stack>
  )
}
