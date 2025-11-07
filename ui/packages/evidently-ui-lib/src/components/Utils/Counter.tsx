import { Box, type SxProps } from '@mui/material'

type CounterProps = {
  sx?: SxProps
  count: number
  unmountIfCountZero?: boolean
}

export const Counter = (props: CounterProps) => {
  const { sx, count, unmountIfCountZero = true } = props

  return (
    <>
      {unmountIfCountZero && count > 0 && (
        <Box
          sx={[
            {
              backgroundColor: 'text.primary',
              color: 'background.default',
              display: 'flex',
              justifyContent: 'center',
              fontWeight: 500,
              alignItems: 'center',
              fontSize: '0.75rem',
              minWidth: '20px',
              height: '20px',
              borderRadius: '10px'
            },

            ...(Array.isArray(sx) ? sx : [sx])
          ]}
        >
          <span>{count}</span>
        </Box>
      )}
    </>
  )
}
