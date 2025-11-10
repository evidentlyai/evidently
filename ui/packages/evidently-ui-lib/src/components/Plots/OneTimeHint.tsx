import { Close as CloseIcon } from '@mui/icons-material'
import { Box, IconButton, Paper, Snackbar, Typography } from '@mui/material'
import { useLocalStorage } from '@uidotdev/usehooks'
import { useEffect, useState } from 'react'

type OneTimeHintProps = {
  storageKey: string
  hintMessage: string
}

export const OneTimeHint = ({ storageKey, hintMessage }: OneTimeHintProps) => {
  const [hasSeenHint, setHasSeenHint] = useLocalStorage(storageKey, false)
  const [isOpen, setIsOpen] = useState(!hasSeenHint)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (!hasSeenHint) {
      setHasSeenHint(true)
    }
  }, [])

  if (!isOpen) {
    return null
  }

  return (
    <Snackbar
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      open={isOpen}
      onClose={(_, reason) => {
        if (reason === 'clickaway') {
          return
        }

        setIsOpen(false)
      }}
    >
      <Paper
        sx={{
          p: 1,
          borderRadius: 2,
          border: '1px solid',
          borderColor: 'divider',
          backgroundColor: 'background.default'
        }}
      >
        <Box display='flex' justifyContent='space-between' alignItems='center' gap={2}>
          <Typography>{hintMessage}</Typography>
          <IconButton size='small' onClick={() => setIsOpen(false)}>
            <CloseIcon />
          </IconButton>
        </Box>
      </Paper>
    </Snackbar>
  )
}
