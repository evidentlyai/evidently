import type { DashboardInfoModel, DatasetPaginationModel } from 'evidently-ui-lib/api/types'
import type { ErrorResponse } from 'evidently-ui-lib/api/types/utils'
import type { DatasetParamsProps } from 'evidently-ui-lib/components/Datasets/types'
import { useUpdateQueryStringValueWithoutNavigation } from 'evidently-ui-lib/hooks/useUpdateQueryStringValueWithoutNavigation'
import { ExpandLess, ExpandMore } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import {
  Box,
  Button,
  Divider,
  Stack,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
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
    <Stack sx={{ maxHeight: 'calc(100vh - 230px)' }} gap={2}>
      <Stack direction={'row'} justifyContent={'center'} gap={2}>
        {datasetStatus === 'success' && (
          <>
            <Button
              variant='outlined'
              onClick={() => setShowDataset((prev) => !prev)}
              startIcon={showDataset ? <ExpandLess /> : <ExpandMore />}
            >
              {showDataset ? 'Hide dataset' : 'Show dataset'}
            </Button>

            <RouterLink
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

      <Box sx={[actuallyShowDataset && { overflow: 'scroll', maxHeight: '40vh' }]}>
        <SnapshotView data={snapshot} projectId={projectId} snapshotId={snapshotId} />
      </Box>

      {actuallyShowDataset && (
        <>
          <Divider />

          <Stack flex={1} minHeight={0}>
            <DatasetViewer
              datasetId={linkedDatasetData.datasetId}
              data={linkedDatasetData.datasetData}
              datasetParams={datasetParams}
              isLoading={isLoading}
            />
          </Stack>
        </>
      )}
    </Stack>
  )
}
