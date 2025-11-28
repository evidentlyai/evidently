import { GenericTabs } from 'evidently-ui-lib/components/Tabs/GenericTabs'
import { Fade } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  useLocation,
  useNavigation,
  useParams
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useMatchRouter, useNavigate } from '~/routes/type-safe-route-helpers/hooks'
import type { GetParamsByPath } from '~/routes/types'

/** Only renders if we are on the project related page */
export const ProjectNavigationTabs = () => {
  const navigate = useNavigate()

  const isOnReportsPages = useMatchRouter({ path: '/projects/:projectId/reports' })
  const isOnDatasetsPages = useMatchRouter({ path: '/projects/:projectId/datasets' })
  const isOnProjectPages = useMatchRouter({ path: '/projects/:projectId' })
  const isOnTracesPages = useMatchRouter({ path: '/projects/:projectId/traces' })
  const isOnPromptsPages = useMatchRouter({ path: '/projects/:projectId/prompts' })

  const { pathname: currentPath } = useLocation()

  const { projectId } = useParams() as Partial<GetParamsByPath<'/projects/:projectId'>>

  const shouldRender = isOnProjectPages && projectId

  const navigation = useNavigation()

  const isLoading = navigation.state !== 'idle'

  if (!shouldRender) {
    return null
  }

  const { activeTab } = {
    activeTab: '?index' as const, // default tab
    ...(isOnReportsPages && { activeTab: 'reports' as const }),
    ...(isOnDatasetsPages && { activeTab: 'datasets' as const }),
    ...(isOnTracesPages && { activeTab: 'traces' as const }),
    ...(isOnPromptsPages && { activeTab: 'prompts' as const })
  }

  return (
    <Fade in timeout={700}>
      <div>
        <GenericTabs
          isLoading={isLoading}
          size='large'
          activeTab={activeTab}
          tabs={
            [
              { key: '?index', label: 'Dashboard' },
              { key: 'reports', label: 'Reports' },
              { key: 'datasets', label: 'Datasets' },
              { key: 'traces', label: 'Traces' },
              { key: 'prompts', label: 'Prompts' }
            ] as const
          }
          onTabChange={(tab) => {
            const normalizePath = (path: string) => path.replace('?index', '').replace(/\/$/, '')

            const goToPath = `/projects/:projectId/${tab}` as const

            const isSamePath =
              normalizePath(currentPath) ===
              normalizePath(goToPath.replace(':projectId', projectId))

            if (isSamePath) {
              return
            }

            navigate({ to: goToPath, paramsToReplace: { projectId } })
          }}
        />
      </div>
    </Fade>
  )
}
