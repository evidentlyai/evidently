import React, { useEffect } from 'react'
import { Alert, AlertTitle, IconButton, Snackbar, Typography, Box } from '@mui/material'
import { isRouteErrorResponse, useActionData, useFetchers, useRouteError } from 'react-router-dom'
import { ErrorData } from '~/api/types/utils'
import type { Fetcher } from 'react-router-dom'
import { Close as CloseIcon } from '@mui/icons-material'

type ActionData = ErrorData | undefined

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
  const actionData = useActionData() as ActionData
  const fetchers = useFetchers() as Fetcher<ActionData>[]
  const [open, setOpen] = React.useState(false)

  const error = actionData?.error || fetchers.find((f) => Boolean(f.data?.error))?.data?.error

  useEffect(() => {
    if (error) {
      setOpen(true)
    }
  }, [error])

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
            {error && (
              <Typography fontWeight={'bold'}>
                {[`Status: ${error.status_code}`, typeof error?.detail === 'string' && error.detail]
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
              onClick={() => setOpen(false)}
            >
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
      </Alert>
    </Snackbar>
  )
}
