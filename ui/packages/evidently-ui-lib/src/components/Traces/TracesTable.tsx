import dayjs from 'dayjs'
import {
  EditDatasetMetadataComponent,
  type UpdateMetadataArgs
} from 'evidently-ui-lib/components/Datasets/Metadata/EditDatasetMetadata'
import { GenericTable } from 'evidently-ui-lib/components/Table/GenericTable'
import { HidedTags } from 'evidently-ui-lib/components/Tags/HidedTags'
import { JsonViewThemed } from 'evidently-ui-lib/components/Utils/JsonView'
import { NameAndID } from 'evidently-ui-lib/components/Utils/NameAndID'
import {
  Close as CloseIcon,
  Delete as DeleteIcon
} from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { Edit as EditIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import {
  Box,
  Chip,
  Dialog,
  DialogContent,
  DialogTitle,
  IconButton,
  Stack,
  Tooltip,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'
import type { DatasetModel } from '~/api/types'

export type TracesTableProps = {
  traces: DatasetModel[]
  GetDatasetLinkByID: (args: { dataset: DatasetModel }) => JSX.Element
  onDelete: (datasetId: string) => void
  isLoading: boolean
  onUpdateMetadata: (args: { datasetId: string; data: UpdateMetadataArgs }) => void
}

export const TracesTable = (props: TracesTableProps) => {
  const { traces, GetDatasetLinkByID, onDelete, onUpdateMetadata, isLoading } = props

  const availableTags = [...new Set(traces.flatMap(({ tags }) => tags))]

  const storageKey = 'favorite-traces-ids'
  const emptyMessage = "You don't have any traces yet."

  return (
    <>
      <GenericTable
        data={traces}
        isLoading={isLoading}
        columns={[
          {
            key: 'trace',
            label: 'Export ID',
            render: (trace) => (
              <Box minWidth={260}>
                <NameAndID name={trace.name} id={trace.id} />
              </Box>
            )
          },
          {
            key: 'description',
            label: 'Description',
            render: (trace) => (
              <Typography
                sx={{
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}
                variant='body2'
              >
                {trace.description}
              </Typography>
            )
          },
          {
            key: 'tags',
            label: 'Tags',
            render: (trace) => (
              <Box minWidth={250}>
                <HidedTags onClick={() => {}} tags={trace.tags} />
              </Box>
            )
          },
          {
            key: 'metadata',
            label: 'Metadata',
            render: (trace) => (
              <Box minWidth={150}>
                <JsonViewThemed value={trace.metadata} enableClipboard={false} />
              </Box>
            )
          },
          {
            key: 'type',
            label: 'Type',
            render: (trace) => <Chip size='medium' label={trace.origin} />
          },
          {
            key: 'created_at',
            label: 'Created at',
            sortable: {
              getSortValue: (trace) => trace.created_at,
              isDateString: true
            },
            render: (trace) => (
              <Typography variant='body2' sx={{ minWidth: 200 }}>
                {dayjs(trace.created_at).locale('en-gb').format('llll')}
              </Typography>
            )
          },
          {
            key: 'actions',
            label: 'Action',
            align: 'center',
            sticky: true,
            render: (trace) => (
              <Stack direction='row' gap={1} alignItems='center' justifyContent={'center'}>
                <GetDatasetLinkByID dataset={trace} />

                <EditTraceDialog
                  trace={trace}
                  availableTags={availableTags}
                  isLoading={isLoading}
                  onUpdateMetadata={(data) =>
                    onUpdateMetadata({
                      datasetId: trace.id,
                      data
                    })
                  }
                />

                <Box>
                  <Tooltip title='delete'>
                    <IconButton
                      disabled={isLoading}
                      size='small'
                      onClick={() => onDelete(trace.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Stack>
            )
          }
        ]}
        idField='id'
        emptyMessage={emptyMessage}
        favorites={{ enabled: true, storageKey }}
        defaultSort={{ column: 'created_at', direction: 'desc' }}
        enableOverflowScroll
      />
    </>
  )
}

type EditTraceDialogProps = {
  trace: DatasetModel
  availableTags: string[]
  isLoading: boolean
  onUpdateMetadata: (args: UpdateMetadataArgs) => void
}

const EditTraceDialog = (props: EditTraceDialogProps) => {
  const { trace, availableTags, isLoading, onUpdateMetadata } = props

  const [open, setOpen] = useState(false)

  return (
    <>
      <Tooltip title='Edit'>
        <span>
          <IconButton disabled={isLoading} onClick={() => setOpen(true)}>
            <EditIcon />
          </IconButton>
        </span>
      </Tooltip>

      <Dialog
        PaperComponent={Box}
        slotProps={{
          paper: {
            sx: {
              backgroundColor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1
            }
          }
        }}
        open={open}
        onClose={() => setOpen(false)}
        fullWidth
        maxWidth='md'
      >
        <DialogTitle>
          <Box display='flex' alignItems='center' justifyContent='space-between'>
            <Typography variant='h6'>Edit Trace</Typography>
            <IconButton onClick={() => setOpen(false)} size='small'>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>

        <DialogContent>
          <Box p={2}>
            <EditDatasetMetadataComponent
              name={trace.name}
              description={trace.description}
              availableTags={availableTags}
              tags={trace.tags ?? []}
              metadata={trace.metadata ?? {}}
              onSave={(data) => {
                onUpdateMetadata(data)

                setOpen(false)
              }}
            />
          </Box>
        </DialogContent>
      </Dialog>
    </>
  )
}
