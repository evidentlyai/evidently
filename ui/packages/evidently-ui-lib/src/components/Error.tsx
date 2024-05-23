import React, { useEffect } from 'react'
import { Alert, AlertTitle, Snackbar, Typography } from '@mui/material'
import { isRouteErrorResponse, useActionData, useRouteError } from 'react-router-dom'
import { ErrorData } from '~/api/types/utils'

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

export const ActionErrorSnackbar = () => {
  const actionData = useActionData() as ErrorData
  const [open, setOpen] = React.useState(false)

  useEffect(() => {
    if (actionData?.error) {
      setOpen(true)
    }
  }, [actionData?.error])

  return (
    <Snackbar
      open={open}
      autoHideDuration={5000}
      onClose={(_, reason) => {
        if (reason === 'clickaway') {
          return
        }

        setOpen(false)
      }}
    >
      <Alert severity="error">
        <AlertTitle>Something went wrong</AlertTitle>
        {actionData?.error && (
          <Typography fontWeight={'bold'}>
            {[
              `Status: ${actionData.error.status_code}`,
              typeof actionData.error?.detail === 'string' && actionData.error.detail
            ]
              .filter(Boolean)
              .join(', ')}
          </Typography>
        )}
      </Alert>
    </Snackbar>
  )
}
