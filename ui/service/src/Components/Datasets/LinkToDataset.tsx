import type { DatasetModel } from 'evidently-ui-lib/api/types'
import { useIsAnyLoaderOrActionRunning } from 'evidently-ui-lib/router-utils/hooks'
import invariant from 'tiny-invariant'
import { useProjectInfo } from '~/contexts/project'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'

type GetDatasetLinkByIDProps = {
  dataset: DatasetModel
}

export const GetDatasetLinkByID = (props: GetDatasetLinkByIDProps) => {
  const { dataset } = props

  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project
  const { id: datasetId } = dataset

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      disabled={isLoading}
      title={'View'}
      // type safe!
      to={'/projects/:projectId/datasets/:datasetId'}
      paramsToReplace={{ projectId, datasetId }}
    />
  )
}
