import { Alert, AlertTitle, Typography } from '@mui/material'
import { isRouteErrorResponse, useRouteError } from 'react-router-dom'

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
    </Alert>
  )
}
