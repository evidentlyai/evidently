import { ViewTimelineOutlined as ViewTimelineOutlinedIcon } from '@mui/icons-material'
import { Box, Button } from '@mui/material'
import type React from 'react'
import { InfoBlock } from './InfoBlock'

type TimelineToggleProps = {
  showTimeline: boolean
  setShowTimeline: React.Dispatch<React.SetStateAction<boolean>>
  isLoading: boolean
}

export const TimelineToggle = (props: TimelineToggleProps) => {
  const { showTimeline, setShowTimeline, isLoading } = props

  return (
    <InfoBlock title={'Timeline'}>
      <Box>
        <Button
          size='small'
          disabled={isLoading}
          onClick={() => setShowTimeline((p) => !p)}
          variant={showTimeline ? 'contained' : 'outlined'}
          startIcon={<ViewTimelineOutlinedIcon />}
        >
          {showTimeline ? 'Hide timeline' : 'Show timeline'}
        </Button>
      </Box>
    </InfoBlock>
  )
}
