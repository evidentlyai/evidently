import { Delete as DeleteIcon } from '@mui/icons-material'
import { Add as AddIcon } from '@mui/icons-material'
import {
  Box,
  Button,
  Chip,
  Collapse,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography
} from '@mui/material'
import { useEffect, useRef } from 'react'
import { TransitionGroup } from 'react-transition-group'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'

export type MessagesPromptVersionState = {
  messages: { id: string; text: string; role: 'user' | 'system' }[]
}

type EditPromptVersionMessagesProps = {
  state: MessagesPromptVersionState
  setState: React.Dispatch<React.SetStateAction<MessagesPromptVersionState>>
}

export type MessagesErrorFields = `message-id-${string}`
const { useErrors, createErrors } = createContextForErrors<MessagesErrorFields>()

export const getMessagesErrors = (state: MessagesPromptVersionState) =>
  createErrors(
    Object.fromEntries(
      state.messages.map((message) => [
        `message-id-${message.id}` satisfies MessagesErrorFields,
        {
          isError: !message.text,
          errorMessage: 'Required'
        }
      ])
    )
  )

export const EditPromptVersionMessages = ({ state, setState }: EditPromptVersionMessagesProps) => {
  const inputRef = useRef<HTMLElement | null>(null)

  const focusOnLast = () => {
    if (!inputRef.current) {
      return
    }

    inputRef.current.focus()
  }

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => focusOnLast(), [state.messages.at(-1)?.id ?? ''])

  const errors = useErrors()

  return (
    <>
      <Box>
        <TransitionGroup>
          {state.messages.map((message) => (
            <Collapse key={message.id}>
              <Stack direction={'row'} useFlexGap gap={2} alignItems={'flex-start'} mb={2}>
                {state.messages.length > 1 && (
                  <Box width={130} sx={{ transform: 'translateY(-8px)' }}>
                    <FormControl fullWidth>
                      <InputLabel>Role</InputLabel>
                      <Select
                        value={message.role}
                        label='Role'
                        renderValue={(value) => <Chip label={value} size='small' />}
                        onChange={(e) =>
                          setState((p) => ({
                            ...p,
                            messages: p.messages.map((m) =>
                              m.id === message.id
                                ? { ...m, role: e.target.value as 'user' | 'system' }
                                : m
                            )
                          }))
                        }
                      >
                        <MenuItem value='user'>
                          <Chip label='user' size='small' />
                        </MenuItem>
                        <MenuItem value='system'>
                          <Chip label='system' size='small' />
                        </MenuItem>
                      </Select>
                    </FormControl>
                  </Box>
                )}

                <TextField
                  {...(state.messages.at(-1)?.id === message.id && { inputRef })}
                  placeholder='Your prompt here'
                  error={errors[`message-id-${message.id}`].isError}
                  helperText={errors[`message-id-${message.id}`].errorMessage}
                  multiline
                  fullWidth
                  value={message.text}
                  onChange={(e) => {
                    const text = e.target.value

                    setState((p) => ({
                      ...p,
                      messages: p.messages.map((m) => (m.id === message.id ? { ...m, text } : m))
                    }))
                  }}
                  sx={{ '& .MuiInputBase-input': { fontFamily: 'monospace', fontSize: '1rem' } }}
                />

                {state.messages.length > 1 && (
                  <IconButton
                    onClick={() =>
                      setState((p) => ({
                        ...p,
                        messages: p.messages.filter((m) => m.id !== message.id)
                      }))
                    }
                  >
                    <DeleteIcon />
                  </IconButton>
                )}
              </Stack>
            </Collapse>
          ))}
        </TransitionGroup>

        <Typography variant='body2' color='text.secondary' mb={2}>
          You can create placeholders in your prompt with curly braces (e.g., {'"{user_feedback}"'})
          to insert values from dataset columns into your prompt.
        </Typography>

        <Box display={'flex'} justifyContent={'center'}>
          <Button
            startIcon={<AddIcon />}
            variant='outlined'
            onClick={() => {
              setState((p) => ({
                ...p,
                messages: [...p.messages, { id: crypto.randomUUID(), role: 'user', text: '' }]
              }))
            }}
          >
            add message
          </Button>
        </Box>
      </Box>
    </>
  )
}
