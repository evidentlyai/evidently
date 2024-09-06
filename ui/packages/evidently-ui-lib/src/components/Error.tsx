import { Close as CloseIcon } from '@mui/icons-material'
import { Alert, AlertTitle, Box, IconButton, Snackbar, Typography } from '@mui/material'
import React, { useEffect } from 'react'
import { isRouteErrorResponse, useActionData, useFetchers, useRouteError } from 'react-router-dom'
import type { Fetcher } from 'react-router-dom'
import type { ErrorData, ErrorResponse } from '~/api/types/utils'

type ActionErrorData = ErrorData | undefined | null

export const GenericErrorBoundary = () => {
  const error = useRouteError()

  return (
    <Alert severity='error'>
      <AlertTitle>Something went wrong</AlertTitle>

      {isRouteErrorResponse(error) && (
        <>
          <Typography fontWeight={'bold'}>
            {[
              `Status: ${error.status}`,
              typeof error.data?.detail === 'string' && error.data.detail
            ]
              .filter(Boolean)
              .join(', ')}
          </Typography>

          {typeof error.data === 'string' && <Typography>{error.data}</Typography>}
        </>
      )}

      {typeof error === 'string' && <Typography fontWeight={'bold'}>{error}</Typography>}
    </Alert>
  )
}

const ErrorAlertSnackBar = ({ data }: { data: ActionErrorData }) => {
  const [open, setOpen] = React.useState(false)
  const error = React.useRef<ErrorResponse | null>(null)

  useEffect(() => {
    if (data?.error) {
      error.current = data.error

      setOpen(true)
    }
  }, [data])

  return (
    <Snackbar
      open={open}
      onClose={(_, reason) => {
        if (reason === 'clickaway') {
          return
        }

        setOpen(false)
      }}
    >
      <Alert severity='error'>
        <Box display={'flex'} justifyContent={'space-between'} alignItems={'flex-start'} gap={2}>
          <Box>
            <AlertTitle>Something went wrong</AlertTitle>
            {error.current && (
              <Typography fontWeight={'bold'}>
                {[
                  typeof error.current.status_code === 'number' &&
                    `Status: ${error.current.status_code}`,
                  typeof error.current.detail === 'string' && error.current.detail
                ]
                  .filter(Boolean)
                  .join(', ')}
              </Typography>
            )}
          </Box>
          <Box>
            <IconButton
              size='small'
              aria-label='close'
              color='inherit'
              onClick={() => {
                setOpen(false)
              }}
            >
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
      </Alert>
    </Snackbar>
  )
}

export const ActionsErrorSnackbar = () => {
  const data = useActionData() as ActionErrorData
  return <ErrorAlertSnackBar data={data} />
}

export const FetchersErrorSnackbar = () => {
  const fetchers = useFetchers() as Fetcher<ActionErrorData>[]
  const data = fetchers.find((f) => Boolean(f.data?.error))?.data

  return <ErrorAlertSnackBar data={data} />
}
