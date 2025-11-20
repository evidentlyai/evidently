import { Delete as DeleteIcon } from '@mui/icons-material'
import { Edit as EditIcon } from '@mui/icons-material'
import { Close as CloseIcon } from '@mui/icons-material'
import {
  Box,
  Chip,
  Dialog,
  DialogContent,
  IconButton,
  Stack,
  Tooltip,
  Typography
} from '@mui/material'
import dayjs from 'dayjs'
import { useState } from 'react'
import type { DatasetModel } from '~/api/types'
import {
  EditDatasetMetadataComponent,
  type UpdateMetadataArgs
} from '~/components/Datasets/Metadata/EditDatasetMetadata'
import { GenericTable } from '~/components/Table/GenericTable'
import { HidedTags } from '~/components/Tags/HidedTags'
import { JsonViewThemed } from '~/components/Utils/JsonView'
import { NameAndID } from '~/components/Utils/NameAndID'

export type DatasetsTableV2Props = {
  datasets: DatasetModel[]
  GetDatasetLinkByID: (args: { dataset: DatasetModel }) => JSX.Element
  onDelete: (datasetId: string) => void
  onUpdateMetadata: (args: {
    datasetId: string
    data: UpdateMetadataArgs
  }) => void
  isLoading: boolean
}

export const DatasetsTableV2 = (props: DatasetsTableV2Props) => {
  const { datasets, GetDatasetLinkByID, onDelete, onUpdateMetadata, isLoading } = props

  const availableTags = Array.from(new Set(datasets.flatMap(({ tags }) => tags)))

  const nameAndIdKeyLabel = { key: 'dataset', label: 'Dataset' }

  const storageKey = 'favourite-datasets-ids'
  const emptyMessage = "You don't have any datasets yet."

  return (
    <>
      <GenericTable
        data={datasets}
        isLoading={isLoading}
        columns={[
          {
            ...nameAndIdKeyLabel,
            render: (dataset) => (
              <Box minWidth={260}>
                <NameAndID name={dataset.name} id={dataset.id} />
              </Box>
            )
          },
          {
            key: 'description',
            label: 'Description',
            render: (dataset) => (
              <Typography
                sx={{
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}
                variant='body2'
              >
                {dataset.description}
              </Typography>
            )
          },
          {
            key: 'tags',
            label: 'Tags',
            render: (dataset) => (
              <Box minWidth={250}>
                <HidedTags onClick={() => {}} tags={dataset.tags} />
              </Box>
            )
          },
          {
            key: 'metadata',
            label: 'Metadata',
            render: (dataset) => (
              <Box minWidth={150}>
                <JsonViewThemed value={dataset.metadata} enableClipboard={false} />
              </Box>
            )
          },
          {
            key: 'type',
            label: 'Type',
            render: (dataset) => <Chip size='medium' label={dataset.origin} />
          },
          {
            key: 'row_count',
            label: 'Rows count',
            sortable: { getSortValue: (dataset) => dataset.row_count },
            render: (dataset) => <Typography variant='body2'>{dataset.row_count}</Typography>
          },
          {
            key: 'created_at',
            label: 'Created at',
            sortable: {
              getSortValue: (dataset) => dataset.created_at,
              isDateString: true
            },
            render: (dataset) => (
              <Typography variant='body2' sx={{ minWidth: 200 }}>
                {dayjs(dataset.created_at).locale('en-gb').format('llll')}
              </Typography>
            )
          },
          {
            key: 'actions',
            label: 'Action',
            align: 'center',
            sticky: true,
            render: (dataset) => (
              <Stack direction='row' gap={1} alignItems='center' justifyContent={'center'}>
                <GetDatasetLinkByID dataset={dataset} />

                <EditDialog
                  dataset={dataset}
                  availableTags={availableTags}
                  isLoading={isLoading}
                  onUpdateMetadata={(data) =>
                    onUpdateMetadata({
                      datasetId: dataset.id,
                      data
                    })
                  }
                />

                <Box>
                  <Tooltip title='delete'>
                    <IconButton
                      disabled={isLoading}
                      size='small'
                      onClick={() => onDelete(dataset.id)}
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

type EditDialogProps = {
  dataset: DatasetModel
  availableTags: string[]
  isLoading: boolean
  onUpdateMetadata: (args: UpdateMetadataArgs) => void
}

const EditDialog = ({ dataset, availableTags, isLoading, onUpdateMetadata }: EditDialogProps) => {
  const [open, setOpen] = useState(false)

  return (
    <>
      <Tooltip title='Edit'>
        <IconButton disabled={isLoading} onClick={() => setOpen(true)}>
          <EditIcon />
        </IconButton>
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
        fullWidth
        maxWidth='md'
        open={open}
        onClose={() => setOpen(false)}
      >
        <DialogContent>
          <Box p={2}>
            <Stack direction={'row'} justifyContent={'flex-end'}>
              <IconButton onClick={() => setOpen(false)}>
                <CloseIcon />
              </IconButton>
            </Stack>

            <EditDatasetMetadataComponent
              name={dataset.name}
              description={dataset.description}
              availableTags={availableTags}
              tags={dataset.tags ?? []}
              metadata={dataset.metadata ?? {}}
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
