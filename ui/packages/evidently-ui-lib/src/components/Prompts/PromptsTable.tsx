import { Delete as DeleteIcon } from '@mui/icons-material'
import { Box, IconButton, Stack, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import type { PromptModel } from '~/api/types'
import { GenericTable } from '~/components/Table/GenericTable'
import { TextWithCopyIcon } from '~/components/Utils/TextWithCopyIcon'

type PromptsTableProps = {
  prompts: PromptModel[]
  GetPromptLinkByID: (args: { promptId: string }) => JSX.Element
  onDelete: (promptId: string) => void
  isLoading: boolean
}
export const PromptsTable = (props: PromptsTableProps) => {
  const { prompts, GetPromptLinkByID, onDelete, isLoading } = props

  return (
    <GenericTable
      isLoading={isLoading}
      data={prompts}
      idField='id'
      emptyMessage="You don't have any prompts yet."
      defaultSort={{ column: 'created_at', direction: 'desc' }}
      favorites={{ enabled: true, storageKey: 'favourite-prompts-ids' }}
      columns={[
        {
          key: 'prompt_id',
          label: 'Prompt ID',
          render: (prompt) => (
            <Stack direction='row' alignItems='center' useFlexGap gap={0.5}>
              <Typography variant='body2'>{prompt.id}</Typography>
              <TextWithCopyIcon showText='' copyText={prompt.id ?? ''} />
            </Stack>
          )
        },
        {
          key: 'name',
          label: 'Name',
          render: (prompt) => (
            <Typography variant='body2' sx={{ maxWidth: 200 }}>
              {prompt.name}
            </Typography>
          )
        },
        {
          key: 'created_at',
          label: 'Created at',
          sortable: {
            getSortValue: (prompt) => prompt.metadata?.created_at,
            isDateString: true
          },
          render: (prompt) => (
            <Typography variant='body2' sx={{ minWidth: 200 }}>
              {dayjs(prompt.metadata?.created_at).locale('en-gb').format('llll')}
            </Typography>
          )
        },
        {
          key: 'actions',
          label: 'Action',
          align: 'center',
          render: (prompt) => (
            <Stack direction='row' gap={1} alignItems='center' justifyContent={'center'}>
              <GetPromptLinkByID promptId={prompt.id ?? 'none'} />
              <Box>
                <Tooltip title='delete'>
                  <IconButton
                    disabled={isLoading}
                    size='small'
                    onClick={() => onDelete(prompt.id ?? '')}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Stack>
          )
        }
      ]}
    />
  )
}
