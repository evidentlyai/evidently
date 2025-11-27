import { zodResolver } from '@hookform/resolvers/zod'
import { Button, Stack, TextField, Typography } from '@mui/material'
import { useForm } from 'evidently-ui-lib/shared-dependencies/react-hook-form'
import { useEffect } from 'react'
import { Form } from 'react-router-dom'
import { z } from 'zod'

const createPromptSchema = z.object({ name: z.string().min(3) })

type DataType = z.infer<typeof createPromptSchema>

type CreatePromptFormProps = {
  onSubmit: (data: DataType) => void
  defaultValues: DataType
  isLoading: boolean
}
export const CreatePromptForm = (props: CreatePromptFormProps) => {
  const { onSubmit, defaultValues, isLoading } = props

  const {
    register,
    handleSubmit,
    setFocus,
    formState: { errors, isDirty }
  } = useForm<z.infer<typeof createPromptSchema>>({
    resolver: zodResolver(createPromptSchema),
    defaultValues
  })

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => setFocus('name'), [])

  return (
    <>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Stack gap={2} maxWidth={'sm'} mx={'auto'}>
          <Typography variant='h5'>Prompt name</Typography>

          <TextField
            size='small'
            error={!!errors.name}
            helperText={errors.name?.message}
            {...register('name')}
          />

          <Stack direction={'row'} justifyContent={'flex-end'}>
            <Button
              disabled={isLoading || !isDirty || Object.keys(errors).length > 0}
              type='submit'
              variant='outlined'
            >
              Submit
            </Button>
          </Stack>
        </Stack>
      </Form>
    </>
  )
}
