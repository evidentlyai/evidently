import {
  PopupState,
  bindPopover,
  bindTrigger
} from 'evidently-ui-lib/shared-dependencies/material-ui-popup-state'
import { Add as AddIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import {
  Button,
  Popover,
  Stack,
  TextField,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'

type AddLabelPopoverProps = {
  additionalLabels: string[]
  setAdditionalLabels: (labels: string[]) => void
  additionalLabelsDisabled: boolean
  zeroEvaluation?: boolean
}

export const AddLabelPopover = (props: AddLabelPopoverProps) => {
  const { additionalLabels, setAdditionalLabels, additionalLabelsDisabled, zeroEvaluation } = props

  const [newLabel, setNewLabel] = useState('')
  const canAddNewLabel = Boolean(newLabel.trim())

  const handleAddNewLabel = () => {
    const label = newLabel.trim()
    if (!label) {
      return
    }

    setAdditionalLabels(Array.from(new Set([...additionalLabels, label])))
    setNewLabel('')
  }

  return (
    <PopupState variant='popover'>
      {(popupState) => (
        <>
          <Button
            size='small'
            startIcon={<AddIcon />}
            variant='outlined'
            disabled={additionalLabelsDisabled}
            {...bindTrigger(popupState)}
          >
            Add custom label
          </Button>
          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
            transformOrigin={{ vertical: 'top', horizontal: 'left' }}
            {...(zeroEvaluation && { elevation: 1 })}
          >
            <Stack direction='column' gap={1} p={2} minWidth={300}>
              <Typography color='text.secondary'>Add a new label:</Typography>

              <TextField
                size='small'
                value={newLabel}
                onChange={(e) => setNewLabel(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && canAddNewLabel) {
                    e.preventDefault()
                    handleAddNewLabel()
                    popupState.close()
                  }
                }}
                placeholder='Type a custom label...'
                fullWidth
              />
              <Stack direction='row' gap={1} justifyContent='flex-end'>
                <Button variant='outlined' size='small' onClick={() => popupState.close()}>
                  Cancel
                </Button>

                <Button
                  variant='contained'
                  size='small'
                  disabled={!canAddNewLabel}
                  onClick={() => {
                    handleAddNewLabel()
                    popupState.close()
                  }}
                >
                  Add
                </Button>
              </Stack>
            </Stack>
          </Popover>
        </>
      )}
    </PopupState>
  )
}
