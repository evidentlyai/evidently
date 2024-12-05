import { Close as CloseIcon } from '@mui/icons-material'
import { Box, Button, IconButton, Link, Paper, Snackbar, Stack, Typography } from '@mui/material'
import { useLocalStorage } from '@uidotdev/usehooks'
import type { PlotMouseEvent } from 'plotly.js'
import { useEffect, useState } from 'react'
import { Link as RLink } from 'react-router-dom'

export type PlotMouseEventType = PlotMouseEvent

export const GoToSnapshotByPoint = ({ event }: { event: PlotMouseEvent }) => {
  const p = event.points[0]
  const customdata = p.customdata as Partial<
    Record<'test_fingerprint' | 'metric_fingerprint' | 'snapshot_id', string>
  >

  const timestamp = p.x && typeof p.x === 'string' ? p.x : null

  if (!customdata) {
    return <></>
  }

  const snapshot_type = 'metric_fingerprint' in customdata ? 'report' : 'test-suite'

  return (
    <>
      <Box
        sx={{
          position: 'absolute',
          bottom: 0,
          right: 0,
          background: (t) => t.palette.background.default,
          p: 1,
          borderRadius: '10px'
        }}
      >
        <Stack direction={'row'} alignItems={'center'} gap={2}>
          {timestamp && (
            <Typography variant='button'>Selected point timestamp: {timestamp}</Typography>
          )}
          <Link component={RLink} to={`${snapshot_type}s/${customdata.snapshot_id}`}>
            <Button variant='outlined'>Go to {snapshot_type}</Button>
          </Link>
        </Stack>
      </Box>
    </>
  )
}

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
          sx={{ p: 1, borderRadius: 2, border: '1px solid', borderColor: (t) => t.palette.divider }}
        >
          <Box display={'flex'} justifyContent={'space-between'} alignItems={'center'} gap={2}>
            <Box>
              <Typography>Click on point in order to go to snapshot</Typography>
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
