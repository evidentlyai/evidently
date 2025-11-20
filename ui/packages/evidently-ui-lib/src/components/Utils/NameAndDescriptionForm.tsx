import { zodResolver } from '@hookform/resolvers/zod'
import { BackupTableOutlined as BackupTableOutlinedIcon } from '@mui/icons-material'
import { Box, Button, Popover, Stack, TextField, Typography } from '@mui/material'
import PopupState, { bindPopover, bindTrigger } from 'material-ui-popup-state'
import { useForm } from 'react-hook-form'
import { Form } from 'react-router-dom'
import { z } from 'zod'

export const nameAndDescriptionSchema = z.object({
  name: z.string().min(3),
  description: z.string().optional().nullable()
})

type NameAndDescriptionFormProps = {
  defaultValues: z.infer<typeof nameAndDescriptionSchema>
  onSubmit: (data: z.infer<typeof nameAndDescriptionSchema>) => void
  submitButtonTitle?: string
  allowSubmitDefaults?: boolean
  isLoading: boolean
}

export const NameAndDescriptionForm = (props: NameAndDescriptionFormProps) => {
  const {
    defaultValues,
    onSubmit,
    submitButtonTitle = 'Save',
    allowSubmitDefaults,
    isLoading
  } = props

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty, isValid }
  } = useForm<z.infer<typeof nameAndDescriptionSchema>>({
    resolver: zodResolver(nameAndDescriptionSchema),
    defaultValues: defaultValues
  })

  return (
    <>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Stack direction={'column'} gap={2} alignItems={'stretch'}>
          <Stack direction={'column'} gap={1}>
            <Typography variant='subtitle2' align='left'>
              Name
            </Typography>
            <TextField
              disabled={isLoading}
              error={!!errors.name?.message}
              helperText={errors.name?.message}
              fullWidth
              size='small'
              placeholder={'name'}
              {...register('name')}
            />
          </Stack>

          <Stack direction={'column'} gap={1}>
            <Typography variant='subtitle2' align='left'>
              Description
            </Typography>

            <TextField
              disabled={isLoading}
              error={!!errors.description?.message}
              helperText={errors.description?.message}
              fullWidth
              size='small'
              placeholder={'Description'}
              {...register('description')}
            />
          </Stack>

          <Stack direction={'row'} justifyContent={'flex-end'}>
            <Button
              disabled={isLoading || !isValid || !(allowSubmitDefaults || isDirty)}
              type='submit'
              variant='outlined'
            >
              {submitButtonTitle}
            </Button>
          </Stack>
        </Stack>
      </Form>
    </>
  )
}

type NameAndDescriptionPopoverProps = {
  formProps: NameAndDescriptionFormProps
  buttonTitle: string
  buttonDisabled?: boolean
}

export const NameAndDescriptionPopover = (props: NameAndDescriptionPopoverProps) => {
  const { formProps, buttonTitle, buttonDisabled = false } = props

  return (
    <PopupState variant='popover'>
      {(popupState) => (
        <>
          <Button
            size='small'
            disabled={buttonDisabled}
            variant='outlined'
            startIcon={<BackupTableOutlinedIcon />}
            {...bindTrigger(popupState)}
          >
            {buttonTitle}
          </Button>

          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            transformOrigin={{ vertical: 'top', horizontal: 'center' }}
          >
            <Box p={2} sx={{ minWidth: 300 }}>
              <NameAndDescriptionForm {...formProps} />
            </Box>
          </Popover>
        </>
      )}
    </PopupState>
  )
}
