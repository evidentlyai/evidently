import { Add as AddIcon } from '@mui/icons-material'
import { Box, Button, Popover, Stack, TextField, Typography } from '@mui/material'
import PopupState, { bindPopover, bindTrigger } from 'material-ui-popup-state'
import { useState } from 'react'

type AddClassButtonProps = {
  onAddClass: (value: string) => void
}

export const AddClassButton = (props: AddClassButtonProps) => {
  const { onAddClass } = props

  const [criteria, setCriteria] = useState('')

  return (
    <>
      <PopupState variant='popover'>
        {(categoryCriteriaPopupState) => (
          <Box>
            <Button
              size='small'
              startIcon={<AddIcon />}
              variant='outlined'
              {...bindTrigger(categoryCriteriaPopupState)}
            >
              add class
            </Button>
            <Popover
              {...bindPopover(categoryCriteriaPopupState)}
              anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
              transformOrigin={{ vertical: 'top', horizontal: 'left' }}
            >
              <Stack direction={'column'} gap={1} p={2} minWidth={300}>
                <Typography variant='body2' color='text.secondary'>
                  Enter the class name:
                </Typography>

                <TextField
                  value={criteria}
                  onChange={(e) => setCriteria(e.target.value)}
                  fullWidth
                  size='small'
                />

                <Stack direction={'row'} gap={1} justifyContent={'flex-end'}>
                  <Button
                    size='small'
                    variant='contained'
                    disabled={!criteria.trim()}
                    onClick={() => {
                      onAddClass(criteria.trim())
                      setCriteria('')
                      categoryCriteriaPopupState.close()
                    }}
                  >
                    Save
                  </Button>
                </Stack>
              </Stack>
            </Popover>
          </Box>
        )}
      </PopupState>
    </>
  )
}
