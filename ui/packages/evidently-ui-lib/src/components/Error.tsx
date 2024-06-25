import React, { useEffect } from 'react'
import { Alert, AlertTitle, IconButton, Snackbar, Typography, Box } from '@mui/material'
import { isRouteErrorResponse, useActionData, useFetchers, useRouteError } from 'react-router-dom'
import { ErrorData } from '~/api/types/utils'
import type { Fetcher } from 'react-router-dom'
import { Close as CloseIcon } from '@mui/icons-material'

type ActionErrorData = ErrorData | undefined | null

export const GenericErrorBoundary = () => {
  const error = useRouteError()

  return (
    <Alert severity="error">
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

  useEffect(() => {
    if (data?.error) {
      setOpen(true)
    }
  }, [data?.error])

  if (!data?.error) {
    return null
  }

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
      <Alert severity="error">
        <Box display={'flex'} justifyContent={'space-between'} alignItems={'flex-start'} gap={2}>
          <Box>
            <AlertTitle>Something went wrong</AlertTitle>
            {data?.error && (
              <Typography fontWeight={'bold'}>
                {[
                  `Status: ${data.error.status_code}`,
                  typeof data.error?.detail === 'string' && data.error.detail
                ]
                  .filter(Boolean)
                  .join(', ')}
              </Typography>
            )}
          </Box>
          <Box>
            <IconButton
              size="small"
              aria-label="close"
              color="inherit"
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
