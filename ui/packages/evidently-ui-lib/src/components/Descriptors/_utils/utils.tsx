import type { PromptTemplate } from '~/api/types'

export const makeEmptyLLMJudgeDescriptorTemplate = (): PromptTemplate => ({
  type: 'evidently:prompt_template:BinaryClassificationPromptTemplate',
  non_target_category: 'NON TARGET',
  target_category: 'TARGET',
  include_category: true,
  uncertainty: 'unknown'
})
