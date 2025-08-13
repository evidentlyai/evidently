import { useIsAnyLoaderOrActionRunning } from 'evidently-ui-lib/router-utils/hooks'
import invariant from 'tiny-invariant'
import { useProjectInfo } from '~/contexts/project'
import { RouterLink } from '~/routes/components'

const GoToSnapshotByPoint = ({ snapshotId }: { snapshotId: string }) => {
  const { project } = useProjectInfo()
  invariant(project)

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      to={'/projects/:projectId/reports/:snapshotId'}
      title='View report'
      variant='outlined'
      paramsToReplace={{ projectId: project.id, snapshotId }}
      disabled={isLoading}
    />
  )
}

export const OnClickedPointComponent = GoToSnapshotByPoint
