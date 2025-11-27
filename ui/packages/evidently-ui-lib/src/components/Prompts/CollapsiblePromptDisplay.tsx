import { ExpandLessSharp as ExpandLessSharpIcon } from '@mui/icons-material'
import { ExpandMoreSharp as ExpandMoreSharpIcon } from '@mui/icons-material'
import { Button, Card, Collapse, Typography } from '@mui/material'
import type React from 'react'

type CollapsiblePromptDisplayProps = {
  details: boolean
  setDetails: React.Dispatch<React.SetStateAction<boolean>>
  buttonTitle?: string
  prompt: string
  isLoading: boolean
}

export const CollapsiblePromptDisplay = (props: CollapsiblePromptDisplayProps) => {
  const { details, setDetails, buttonTitle, prompt, isLoading } = props

  return (
    <>
      <Button
        variant='outlined'
        startIcon={details ? <ExpandLessSharpIcon /> : <ExpandMoreSharpIcon />}
        onClick={() => setDetails((prev) => !prev)}
      >
        {buttonTitle ?? 'Show final prompt'}
      </Button>

      <Collapse in={Boolean(details && prompt)} unmountOnExit sx={{ width: 1 }}>
        <Card
          sx={{
            p: 3,
            my: 1,
            opacity: isLoading ? 0.5 : 1,
            border: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Typography
            component='pre'
            sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces', fontSize: '1rem' }}
          >
            {prompt}
          </Typography>
        </Card>
      </Collapse>
    </>
  )
}
