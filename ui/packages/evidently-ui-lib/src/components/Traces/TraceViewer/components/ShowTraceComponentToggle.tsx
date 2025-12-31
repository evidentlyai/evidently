import { FeedbackOutlined as FeedbackIcon } from '@mui/icons-material'
import { Box, Button } from '@mui/material'
import type React from 'react'
import { InfoBlock } from './InfoBlock'

type ShowTraceComponentToggleProps = {
  showTraceComponent: boolean
  setShowTraceComponent: React.Dispatch<React.SetStateAction<boolean>>
}

export const ShowTraceComponentToggle = (props: ShowTraceComponentToggleProps) => {
  const { showTraceComponent, setShowTraceComponent } = props

  return (
    <InfoBlock title={'Show feedback'}>
      <Box>
        <Button
          size='small'
          onClick={() => setShowTraceComponent((p) => !p)}
          variant={showTraceComponent ? 'contained' : 'outlined'}
          startIcon={<FeedbackIcon />}
        >
          {showTraceComponent ? 'Hide feedback' : 'Show feedback'}
        </Button>
      </Box>
    </InfoBlock>
  )
}
