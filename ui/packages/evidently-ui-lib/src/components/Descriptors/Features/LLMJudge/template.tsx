import { Delete as DeleteIcon } from '@mui/icons-material'
import {
  Autocomplete,
  Box,
  Button,
  Chip,
  FormControl,
  FormHelperText,
  Stack,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
  Typography
} from '@mui/material'
import type { PromptTemplate } from '~/api/types'
import { AddClassButton } from '~/components/Descriptors/_utils/AddClassButton'
import { CategoryScoreReasoning } from '~/components/Descriptors/_utils/ReasoningCategoryScore'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { GenericTable } from '~/components/Table/GenericTable'

export type TemplateErrorFields =
  | 'reasoning_category_score'
  // multiclass
  | `classes`
  | `class-criteria-${string}`
  // binary
  | 'main_criteria'
  | 'target'
  | 'non_target'
  | 'uncertainty'

const { useErrors, createErrors } = createContextForErrors<TemplateErrorFields>()

type LLMJudgeTemplateFeatureEditorProps = {
  state: PromptTemplate
  setState: React.Dispatch<React.SetStateAction<PromptTemplate>>
}

export const getLLMJudgeTemplateErrors = (state: PromptTemplate) =>
  createErrors({
    ...Object.fromEntries(
      Object.entries(
        state.type === 'evidently:prompt_template:MulticlassClassificationPromptTemplate'
          ? (state.category_criteria ?? {})
          : {}
      ).map(([className, classCriteria]) => [
        `class-criteria-${className}` satisfies TemplateErrorFields,
        {
          isError: !classCriteria,
          errorMessage: `Provide criteria for class "${className}"`
        }
      ])
    ),
    classes: {
      isError:
        state.type === 'evidently:prompt_template:MulticlassClassificationPromptTemplate' &&
        Object.keys(state.category_criteria ?? {}).length === 0,
      errorMessage: 'Provide at least one class'
    },
    reasoning_category_score: {
      isError: !state.include_reasoning && !state.include_score && !state.include_category,
      errorMessage: 'Select at least one option'
    },
    target: {
      isError:
        state.type === 'evidently:prompt_template:BinaryClassificationPromptTemplate' &&
        !state.target_category,
      errorMessage: 'Required'
    },
    non_target: {
      isError:
        state.type === 'evidently:prompt_template:BinaryClassificationPromptTemplate' &&
        !state.non_target_category,
      errorMessage: 'Required'
    },
    uncertainty: {
      isError: !state.uncertainty,
      errorMessage: 'Required'
    },
    main_criteria: {
      isError: !state.criteria,
      errorMessage: 'Required'
    }
  })

export const LLMJudgeTemplateEditor = (props: LLMJudgeTemplateFeatureEditorProps) => {
  const { state, setState } = props

  const errors = useErrors()

  return (
    <>
      <Stack>
        <Typography variant='h6' gutterBottom>
          Criteria
        </Typography>

        <TextField
          multiline
          fullWidth
          error={errors.main_criteria.isError}
          helperText={errors.main_criteria.errorMessage}
          value={state.criteria ?? ''}
          onChange={({ target: { value: criteria } }) => setState({ ...state, criteria })}
        />

        <Typography mt={1} variant='body2' color='text.secondary'>
          You can create additional placeholders in your prompt criteria with curly braces (e.g.,
          {'"{user_feedback}"'}) to insert values from dataset columns into your prompt.
        </Typography>
      </Stack>

      <Stack>
        <Typography variant='h6' gutterBottom>
          Classification mode
        </Typography>

        <ToggleButtonGroup
          size='small'
          value={state.type ?? ''}
          exclusive
          onChange={(_, type) => {
            if (!type) {
              return
            }

            setState({
              ...state,
              type,
              ...((type as PromptTemplate['type']) ===
                'evidently:prompt_template:MulticlassClassificationPromptTemplate' && {
                // force uncertainty to unknown for multiclass classification mode
                uncertainty: 'unknown'
              })
            })
          }}
        >
          {(
            [
              {
                label: 'Binary',
                value: 'evidently:prompt_template:BinaryClassificationPromptTemplate'
              },
              {
                label: 'Multiclass',
                value: 'evidently:prompt_template:MulticlassClassificationPromptTemplate'
              }
            ] satisfies {
              label: string
              value: PromptTemplate['type']
            }[]
          ).map((value) => (
            <ToggleButton key={value.label} value={value.value}>
              {value.label}
            </ToggleButton>
          ))}
        </ToggleButtonGroup>
      </Stack>

      {state.type === 'evidently:prompt_template:BinaryClassificationPromptTemplate' && (
        <Stack my={1} direction={'row'} gap={2} alignItems={'flex-start'}>
          <Stack width={230}>
            <Typography color={'text.secondary'} variant='subtitle2' gutterBottom>
              Target category
            </Typography>

            <TextField
              size='small'
              value={state.target_category ?? ''}
              error={errors.target.isError}
              helperText={errors.target.errorMessage}
              onChange={({ target: { value: target_category } }) =>
                setState({ ...state, target_category })
              }
            />
          </Stack>

          <Stack width={230}>
            <Typography color={'text.secondary'} variant='subtitle2' gutterBottom>
              Non target category
            </Typography>

            <TextField
              size='small'
              value={state.non_target_category ?? ''}
              error={errors.non_target.isError}
              helperText={errors.non_target.errorMessage}
              onChange={({ target: { value: non_target_category } }) =>
                setState({ ...state, non_target_category })
              }
            />
          </Stack>

          <Box width={230}>
            <FormControl size='small' fullWidth error={errors.uncertainty.isError}>
              <Typography color={'text.secondary'} variant='subtitle2' gutterBottom>
                Uncertain category
              </Typography>

              <Autocomplete
                value={state.uncertainty}
                onChange={(_, value) => setState({ ...state, uncertainty: value ?? undefined })}
                options={['unknown', 'target', 'non_target'] as const}
                renderValue={(value, getItemProps) => {
                  if (!value) return null
                  const itemProps = getItemProps()
                  return <Chip variant='filled' size='small' label={value} {...itemProps} />
                }}
                renderInput={(params) => (
                  <TextField error={errors.uncertainty.isError} {...params} variant='outlined' />
                )}
                size='small'
              />

              {errors.uncertainty.errorMessage && (
                <FormHelperText>{errors.uncertainty.errorMessage}</FormHelperText>
              )}
            </FormControl>
          </Box>
        </Stack>
      )}

      {state.type === 'evidently:prompt_template:MulticlassClassificationPromptTemplate' && (
        <Stack>
          <Typography variant='h6'>Classes</Typography>

          <Typography variant='body2' color='text.secondary' gutterBottom>
            Provide classes for multiclass classification mode.
          </Typography>

          {errors.classes.isError && (
            <Typography color={'error'} variant='subtitle2' fontWeight={400} fontSize={'0.75rem'}>
              {errors.classes.errorMessage}
            </Typography>
          )}

          <Stack mt={1} gap={2}>
            {Object.entries(state.category_criteria ?? {}).length > 0 && (
              <Stack direction={'row'} gap={2} flexWrap={'wrap'}>
                {Object.entries(state.category_criteria ?? {}).map(([className, classCriteria]) => (
                  <Box
                    key={className}
                    p={2}
                    border={1}
                    borderColor='divider'
                    borderRadius={1}
                    flex={'1 0 calc(50% - 8px)'}
                  >
                    <Stack direction={'column'} gap={1}>
                      <Stack
                        direction={'row'}
                        justifyContent={'space-between'}
                        alignItems={'center'}
                      >
                        <Stack direction={'row'} gap={1} alignItems={'center'}>
                          <Typography variant='h6'>Class</Typography>

                          <Chip
                            label={className}
                            variant='filled'
                            sx={{ fontWeight: 'bold', fontSize: '1.25rem' }}
                          />
                        </Stack>

                        <Button
                          size='small'
                          startIcon={<DeleteIcon />}
                          variant='outlined'
                          onClick={() => {
                            if (
                              state.type !==
                              'evidently:prompt_template:MulticlassClassificationPromptTemplate'
                            ) {
                              return
                            }

                            setState({
                              ...state,
                              category_criteria: Object.fromEntries(
                                Object.entries(state.category_criteria ?? {}).filter(
                                  ([k]) => k !== className
                                )
                              )
                            })
                          }}
                        >
                          Delete
                        </Button>
                      </Stack>

                      <Stack>
                        <Typography variant='body2' color='text.secondary' gutterBottom>
                          Criteria for "{className}" class
                        </Typography>

                        <TextField
                          fullWidth
                          multiline
                          size='small'
                          value={classCriteria}
                          error={errors?.[`class-criteria-${className}`]?.isError}
                          helperText={errors?.[`class-criteria-${className}`]?.errorMessage}
                          onChange={({ target: { value } }) => {
                            if (
                              state.type !==
                              'evidently:prompt_template:MulticlassClassificationPromptTemplate'
                            ) {
                              return
                            }

                            setState({
                              ...state,
                              category_criteria: { ...state.category_criteria, [className]: value }
                            })
                          }}
                        />
                      </Stack>
                    </Stack>
                  </Box>
                ))}
              </Stack>
            )}

            <AddClassButton
              onAddClass={(value) => {
                if (
                  state.type !== 'evidently:prompt_template:MulticlassClassificationPromptTemplate'
                ) {
                  return
                }

                setState({
                  ...state,
                  category_criteria: { ...(state.category_criteria ?? {}), [value]: '' }
                })
              }}
            />
          </Stack>
        </Stack>
      )}

      <Stack>
        <Typography variant='h6' gutterBottom>
          Output
        </Typography>

        <CategoryScoreReasoning
          values={{
            include_category: state.include_category,
            include_reasoning: state.include_reasoning,
            include_score: state.include_score
          }}
          setValues={(values) =>
            setState({
              ...state,
              include_category: values.include_category ?? undefined,
              include_reasoning: values.include_reasoning ?? undefined,
              include_score: values.include_score ?? undefined
            })
          }
          error={errors.reasoning_category_score.isError}
          errorMessage={errors.reasoning_category_score.errorMessage}
        />
      </Stack>
    </>
  )
}

type LLMJudgeTemplateViewerProps = {
  state: PromptTemplate
  additionalHeaderElements?: React.ReactNode
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

export const LLMJudgeTemplateViewer = (props: LLMJudgeTemplateViewerProps) => {
  const { state, additionalHeaderElements, PromptViewerComponent } = props

  return (
    <Stack gap={2}>
      <Stack direction='row' gap={5} alignItems='flex-start'>
        {additionalHeaderElements}

        <Stack>
          <Typography variant='h6'>Classification mode</Typography>

          <Box>
            <Chip
              variant='filled'
              label={
                state.type === 'evidently:prompt_template:BinaryClassificationPromptTemplate'
                  ? 'Binary'
                  : state.type ===
                      'evidently:prompt_template:MulticlassClassificationPromptTemplate'
                    ? 'Multiclass'
                    : '—'
              }
            />
          </Box>
        </Stack>

        {state.type === 'evidently:prompt_template:BinaryClassificationPromptTemplate' && (
          <Stack>
            <Typography variant='h6'>Categories & uncertainty</Typography>
            <Box border={1} borderColor='divider' borderRadius={1}>
              <GenericTable
                removeLastBorderBottom
                data={[
                  {
                    id: 0,
                    target_category: state.target_category,
                    non_target_category: state.non_target_category,
                    uncertainty: state.uncertainty
                  }
                ]}
                columns={[
                  {
                    key: 'target_category',
                    label: 'Target',
                    render: (value) => <Chip variant='filled' label={value.target_category} />
                  },
                  {
                    key: 'non_target_category',
                    label: 'Non-target',
                    render: (value) => <Chip variant='filled' label={value.non_target_category} />
                  },

                  {
                    key: 'uncertainty',
                    label: 'Uncertain',
                    render: (value) => <Chip variant='filled' label={value.uncertainty ?? ''} />
                  }
                ]}
                idField='id'
              />
            </Box>
          </Stack>
        )}

        {state.type === 'evidently:prompt_template:MulticlassClassificationPromptTemplate' && (
          <Stack>
            <Typography variant='h6'>Classes</Typography>

            <Stack direction='row' gap={1} alignItems='center' flexWrap='wrap'>
              {Object.keys(state.category_criteria ?? {}).map((className) => (
                <Chip key={className} variant='filled' label={className} />
              ))}
            </Stack>
          </Stack>
        )}
      </Stack>

      <Stack>
        <Typography variant='h6' gutterBottom>
          Criteria
        </Typography>

        <Box
          component='pre'
          sx={{
            p: 2,
            bgcolor: 'action.hover',
            borderRadius: 0.5,
            whiteSpace: 'pre-wrap',
            fontFamily: 'monospace',
            border: '1px solid',
            borderColor: 'divider'
          }}
        >
          {state.criteria}
        </Box>
      </Stack>

      <Stack>
        <Typography variant='h6' gutterBottom>
          Output
        </Typography>

        <Stack direction='row' gap={1} alignItems='center' flexWrap='wrap'>
          {[
            { key: 'reasoning', on: Boolean(state.include_reasoning) },
            { key: 'category', on: Boolean(state.include_category) },
            { key: 'score', on: Boolean(state.include_score) }
          ]
            .filter(({ on }) => on)
            .map(({ key }) => (
              <Box
                key={key}
                component='code'
                sx={{ px: 0.75, py: 0.25, bgcolor: 'action.hover', borderRadius: 0.5 }}
              >
                {key}
              </Box>
            ))}
        </Stack>
      </Stack>

      <Stack alignItems={'flex-start'}>
        <PromptViewerComponent data={state} />
      </Stack>
    </Stack>
  )
}
