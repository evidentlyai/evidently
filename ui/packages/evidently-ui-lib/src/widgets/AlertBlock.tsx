import type React from 'react'
import { type ReactNode, useState } from 'react'

import { Paper, Popover, Typography } from '@mui/material'
import type { Theme } from '@mui/material/styles'

import { darken, lighten } from '@mui/material/styles'

import type { MetricAlertParams } from '~/api'

interface AlertBlockProps {
  data: MetricAlertParams
  customPopup?: ReactNode
}

function getBackgroundColor(theme: Theme) {
  return theme.palette.mode === 'dark' ? lighten : darken
}

function getColor(theme: Theme) {
  return theme.palette.mode === 'light' ? darken : lighten
}

interface PopoverState {
  open: boolean
  anchorEl?: EventTarget & HTMLElement
}

const AlertBlock: React.FunctionComponent<AlertBlockProps> = (props) => {
  const [state, setState] = useState<PopoverState>({ open: false })
  return (
    <Paper
      elevation={0}
      onClick={(event) => setState((s) => ({ open: !s.open, anchorEl: event.currentTarget }))}
      sx={[
        // info by default
        {
          color: (theme) => getColor(theme)(theme.palette.info.main, 0.6),
          backgroundColor: (theme) => getBackgroundColor(theme)(theme.palette.info.main, 0.9)
        },
        props.data.state === 'success' && {
          color: (theme) => getColor(theme)(theme.palette.success.main, 0.6),
          backgroundColor: (theme) => getBackgroundColor(theme)(theme.palette.success.main, 0.9)
        },
        props.data.state === 'warning' && {
          color: (theme) => getColor(theme)(theme.palette.warning.main, 0.6),
          backgroundColor: (theme) => getBackgroundColor(theme)(theme.palette.warning.main, 0.9)
        },
        props.data.state === 'error' && {
          color: (theme) => getColor(theme)(theme.palette.error.main, 0.6),
          backgroundColor: (theme) => getBackgroundColor(theme)(theme.palette.error.main, 0.9)
        }
      ]}
    >
      <Typography align={'center'} variant={'h6'} component={'div'}>
        {props.data.value}
      </Typography>
      <Typography align={'center'} variant={'body1'} component={'div'}>
        {props.data.text}
      </Typography>
      <Popover
        open={state.open}
        anchorEl={state.anchorEl}
        anchorOrigin={{ horizontal: 'left', vertical: 'bottom' }}
      >
        {props.customPopup ?? <Typography padding={1}>{props.data.longText}</Typography>}
      </Popover>
    </Paper>
  )
}

export default AlertBlock
