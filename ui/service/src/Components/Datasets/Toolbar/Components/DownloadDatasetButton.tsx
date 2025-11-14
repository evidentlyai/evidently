import type { BackendPaths } from 'evidently-ui-lib/api/types'
import {
  PopupState,
  bindPopover,
  bindTrigger
} from 'evidently-ui-lib/shared-dependencies/material-ui-popup-state'
import { FileDownload as FileDownloadIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import {
  Box,
  Button,
  MenuItem,
  Popover,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'

const downloadDatasetPath = '/api/datasets/{dataset_id}/download' as const

type DownloadDatasetPath = Extract<keyof BackendPaths, typeof downloadDatasetPath>
type DownloadDatasetQueryKeys = keyof Exclude<
  BackendPaths[DownloadDatasetPath]['get']['parameters']['query'],
  undefined
>

const downloadDatasetUrlTemplate: DownloadDatasetPath = downloadDatasetPath

const getDownloadCSVURL = ({ datasetId }: { datasetId: string }) => {
  const url = downloadDatasetUrlTemplate.replace('{dataset_id}', datasetId)
  const format = 'format' satisfies DownloadDatasetQueryKeys

  return `${url}?${format}=${encodeURIComponent('csv+file')}`
}

export type DownloadDatasetButtonProps = {
  datasetId: string
}

export const DownloadDatasetButton = (props: DownloadDatasetButtonProps) => {
  const { datasetId } = props

  return (
    <PopupState variant='popover'>
      {(popupState) => (
        <Box>
          <Button size='small' startIcon={<FileDownloadIcon />} {...bindTrigger(popupState)}>
            Export
          </Button>

          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'center' }}
          >
            <Box py={1}>
              <MenuItem
                onClick={() => {
                  const csvUrl = getDownloadCSVURL({ datasetId })
                  window.open(csvUrl)
                }}
              >
                <Typography>Download as CSV</Typography>
              </MenuItem>
            </Box>
          </Popover>
        </Box>
      )}
    </PopupState>
  )
}
