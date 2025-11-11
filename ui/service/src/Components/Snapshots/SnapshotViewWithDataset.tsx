import type { DashboardInfoModel, DatasetPaginationModel } from 'evidently-ui-lib/api/types'
import type { ErrorResponse } from 'evidently-ui-lib/api/types/utils'
import type { DatasetParamsProps } from 'evidently-ui-lib/components/Datasets/types'
import { useUpdateQueryStringValueWithoutNavigation } from 'evidently-ui-lib/hooks/useUpdateQueryStringValueWithoutNavigation'
import { ExpandLess, ExpandMore } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { Box, Button, Stack, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useSearchParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useState } from 'react'
import { DatasetViewer } from '~/Components/Datasets/DatasetViewer'
import { SnapshotView } from '~/Components/Snapshots/SnapshotView'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'

type LinkedDatasetData =
  | { type: 'no_linking_dataset' }
  | { type: 'success'; datasetId: string; datasetData: DatasetPaginationModel }
  | { type: 'error'; error: ErrorResponse }

type SnapshotViewWithDatasetProps = {
  snapshot: DashboardInfoModel
  projectId: string
  snapshotId: string
  linkedDatasetData: LinkedDatasetData
  datasetParams: DatasetParamsProps
  isLoading: boolean
}

export const SnapshotViewWithDataset = (props: SnapshotViewWithDatasetProps) => {
  const { snapshot, projectId, snapshotId, linkedDatasetData, datasetParams, isLoading } = props
  const { type: datasetStatus } = linkedDatasetData

  const hideDatasetKey = 'hide-dataset'

  const [searchParams] = useSearchParams()
  const hideDatasetDefault = searchParams.get(hideDatasetKey)

  const [showDataset, setShowDataset] = useState(!hideDatasetDefault)
  useUpdateQueryStringValueWithoutNavigation(hideDatasetKey, !showDataset ? 'true' : '')

  const actuallyShowDataset = datasetStatus === 'success' && showDataset

  if (datasetStatus === 'no_linking_dataset') {
    return <SnapshotView data={snapshot} projectId={projectId} snapshotId={snapshotId} />
  }

  return (
    <Stack gap={2}>
      <Stack direction={'row'} justifyContent={'center'} gap={2}>
        {datasetStatus === 'success' && (
          <>
            <Button
              size='small'
              variant='outlined'
              onClick={() => setShowDataset((prev) => !prev)}
              startIcon={showDataset ? <ExpandLess /> : <ExpandMore />}
            >
              {showDataset ? 'Hide dataset' : 'Show dataset'}
            </Button>

            <RouterLink
              size='small'
              variant='contained'
              type='button'
              title='Go to dataset'
              to={'/projects/:projectId/datasets/:datasetId'}
              paramsToReplace={{ projectId, datasetId: linkedDatasetData.datasetId }}
            />
          </>
        )}

        {datasetStatus === 'error' && (
          <Typography variant='body1' color='error' align='center' gutterBottom>
            Failed to load linked dataset: {linkedDatasetData.error.detail}
          </Typography>
        )}
      </Stack>

      <Box
        sx={[
          actuallyShowDataset && {
            maxHeight: '50vh',
            overflow: 'scroll',
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            p: 1.5
          }
        ]}
      >
        <SnapshotView data={snapshot} projectId={projectId} snapshotId={snapshotId} />
      </Box>

      {actuallyShowDataset && (
        <Stack minHeight={'30vh'} maxHeight={'60vh'}>
          <DatasetViewer
            datasetId={linkedDatasetData.datasetId}
            data={linkedDatasetData.datasetData}
            datasetParams={datasetParams}
            isLoading={isLoading}
          />
        </Stack>
      )}
    </Stack>
  )
}
