import { Box, Card, Chip, Collapse, Stack, Typography } from '@mui/material'
import dayjs from 'dayjs'
import type React from 'react'
import { TransitionGroup } from 'react-transition-group'
import type { PromptVersionModel } from '~/api/types'

export type PromptVersionsSidebarProps = {
  promptVersions: PromptVersionModel[]
  latestPromptVersion: PromptVersionModel | null
  selectedPromptVersionId: string | null
  onChangeSelectedPromptVersionId: (promptId: string) => void
  createNewVersionButton: React.ReactNode
}

export const PromptVersionsSidebar = (props: PromptVersionsSidebarProps) => {
  const {
    promptVersions,
    latestPromptVersion,
    selectedPromptVersionId,
    onChangeSelectedPromptVersionId,
    createNewVersionButton
  } = props

  return (
    <Box height={1} sx={[{ borderRight: '1px solid', borderRightColor: 'divider' }]}>
      <Box
        position={'sticky'}
        top={0}
        left={0}
        sx={{ backgroundColor: 'background.paper' }}
        py={2}
        zIndex={30}
      >
        <Stack direction={'column'} gap={1} alignItems={'center'}>
          <Typography align='center'>Prompt versions</Typography>

          {createNewVersionButton}
        </Stack>
      </Box>

      <Box mt={1} width={1} maxWidth={500} mx={'auto'} px={2}>
        <TransitionGroup>
          {promptVersions.map((promptVersion) => (
            <Collapse key={promptVersion.id}>
              <Box my={1}>
                <Card
                  onClick={() => onChangeSelectedPromptVersionId(promptVersion.id ?? '')}
                  sx={[
                    {
                      p: 1,
                      cursor: 'pointer',
                      transition: (t) =>
                        t.transitions.create(['background-color'], {
                          duration: t.transitions.duration.standard
                        }),
                      '&:hover': (t) => ({
                        backgroundColor: '#f6f6f6',
                        ...t.applyStyles('dark', { backgroundColor: 'divider' })
                      })
                    },
                    promptVersion.id === selectedPromptVersionId && {
                      borderColor: 'primary.main'
                    }
                  ]}
                >
                  <Stack gap={1}>
                    <Stack direction={'row'} gap={1}>
                      <Chip variant='outlined' size='small' label={`#${promptVersion.version}`} />

                      {promptVersion.id === latestPromptVersion?.id && (
                        <Chip size='small' label={'latest'} variant='filled' color='primary' />
                      )}
                    </Stack>

                    <Typography variant='body2'>
                      Created:{' '}
                      {dayjs(promptVersion.metadata?.created_at).locale('en-gb').format('llll')}
                    </Typography>
                  </Stack>
                </Card>
              </Box>
            </Collapse>
          ))}
        </TransitionGroup>
      </Box>
    </Box>
  )
}
