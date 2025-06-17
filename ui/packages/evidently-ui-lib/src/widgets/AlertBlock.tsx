import { Paper, Popover, Typography } from '@mui/material'
import { alpha } from '@mui/material/styles'
import type React from 'react'
import { type ReactNode, useState } from 'react'
import type { MetricAlertParams } from '~/api'

interface AlertBlockProps {
  data: MetricAlertParams
  customPopup?: ReactNode
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
        {
          border: '1px solid',
          borderColor: 'divider'
        },
        {
          color: (theme) => alpha(theme.vars.palette[props?.data?.state ?? 'info'].main, 0.6),
          backgroundColor: (theme) =>
            alpha(theme.vars.palette[props?.data?.state ?? 'info'].main, 0.1)
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
