import { Close as CloseIcon } from '@mui/icons-material'
import { Box, IconButton, Paper, Snackbar, Typography } from '@mui/material'
import { useLocalStorage } from '@uidotdev/usehooks'
import type { PlotMouseEvent } from 'plotly.js'
import { useEffect, useState } from 'react'

export type PlotMouseEventType = PlotMouseEvent

export const HintOnHoverToPlot = () => {
  const [isSawHint, setIsSawHint] = useLocalStorage('is-user-saw-click-on-datapoints-hint', false)

  const [open, setOpen] = useState(!isSawHint)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => setIsSawHint(true), [])

  if (!open) {
    return <></>
  }

  return (
    <>
      <Snackbar
        open={open}
        onClose={(_, reason) => {
          if (reason === 'clickaway') {
            return
          }

          setOpen(false)
        }}
      >
        <Paper
          sx={{
            p: 1,
            borderRadius: 2,
            border: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Box display={'flex'} justifyContent={'space-between'} alignItems={'center'} gap={2}>
            <Box>
              <Typography>You can click on the data point to open the Report.</Typography>
            </Box>
            <Box>
              <IconButton
                size='small'
                onClick={() => {
                  setOpen(false)
                }}
              >
                <CloseIcon />
              </IconButton>
            </Box>
          </Box>
        </Paper>
      </Snackbar>
    </>
  )
}
