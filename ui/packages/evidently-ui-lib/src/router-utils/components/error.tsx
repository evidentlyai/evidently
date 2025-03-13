import { Close as CloseIcon } from '@mui/icons-material'
import { AlertTitle, Box, IconButton, Snackbar, Typography } from '@mui/material'
import React, { useEffect, useState } from 'react'
import { isRouteErrorResponse, useActionData, useFetchers, useRouteError } from 'react-router-dom'
import type { Fetcher } from 'react-router-dom'
import type { ErrorData, ErrorResponse } from '~/api/types/utils'
import { AlertThemed } from '~/components/AlertThemed'

type ActionErrorData = ErrorData | undefined | null

export const GenericErrorBoundary = () => {
  const error = useRouteError()

  console.error(error)

  const classicErrorMessage =
    (typeof error === 'object' &&
      error &&
      'message' in error &&
      typeof error.message === 'string' &&
      error.message) ||
    (typeof error === 'string' && error)

  return (
    <Box p={2}>
      <AlertThemed severity='error'>
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

        {typeof classicErrorMessage === 'string' && (
          <Typography fontWeight={'bold'}>{classicErrorMessage}</Typography>
        )}
      </AlertThemed>
    </Box>
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
      <Box>
        <AlertThemed severity='error' forseFilled>
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
        </AlertThemed>
      </Box>
    </Snackbar>
  )
}

export const ActionsErrorSnackbar = () => {
  const data = useActionData() as ActionErrorData
  return <ErrorAlertSnackBar data={data} />
}

export const FetchersErrorSnackbar = () => {
  const [lastActiveFetcherIndex, setLastActiveFetcherIndex] = useState(0)

  const fetchers = useFetchers() as Fetcher<ActionErrorData>[]
  const isSomeIsNotIdle = fetchers.some((e) => e.state !== 'idle')
  const isAllFetchersIdle = !isSomeIsNotIdle

  useEffect(() => {
    if (isSomeIsNotIdle) {
      const idnex = fetchers.findLastIndex((e) => e.state !== 'idle')

      if (idnex > -1) {
        setLastActiveFetcherIndex(idnex)
      }
    }
  }, [isSomeIsNotIdle, fetchers])

  const d = isAllFetchersIdle && fetchers?.[lastActiveFetcherIndex]?.data

  const data = d && typeof d === 'object' && 'error' in d ? d : undefined

  return <ErrorAlertSnackBar data={data} />
}

// use this only on top level routes
export const handleFetchersActionErrors = ({ Component }: { Component: React.ComponentType }) => ({
  Component: () => (
    <>
      <FetchersErrorSnackbar />
      <Component />
    </>
  )
})
