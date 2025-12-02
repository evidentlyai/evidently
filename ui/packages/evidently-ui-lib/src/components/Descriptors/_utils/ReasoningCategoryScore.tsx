import { Checkbox, FormControl, FormControlLabel, Typography } from '@mui/material'

type Values = {
  include_reasoning?: boolean | null
  include_score?: boolean | null
  include_category?: boolean | null
}

type CategoryScoreReasoningProps = {
  values: Values
  setValues: (values: Values) => void
  error?: boolean
  errorMessage?: string
}

export const CategoryScoreReasoning = (props: CategoryScoreReasoningProps) => {
  const { values, setValues, error, errorMessage } = props

  return (
    <FormControl sx={{ display: 'inline-block' }} error={error}>
      <FormControlLabel
        control={
          <Checkbox
            checked={values.include_reasoning ?? false}
            onChange={(e) => setValues({ ...values, include_reasoning: e.target.checked })}
          />
        }
        label='Reasoning'
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={values.include_category ?? false}
            onChange={(e) => setValues({ ...values, include_category: e.target.checked })}
          />
        }
        label='Category'
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={values.include_score ?? false}
            onChange={(e) => setValues({ ...values, include_score: e.target.checked })}
          />
        }
        label='Score'
      />

      {error && (
        <Typography
          mt={0.5}
          color={'error'}
          variant='subtitle2'
          fontWeight={400}
          fontSize={'0.75rem'}
        >
          {errorMessage}
        </Typography>
      )}
    </FormControl>
  )
}
