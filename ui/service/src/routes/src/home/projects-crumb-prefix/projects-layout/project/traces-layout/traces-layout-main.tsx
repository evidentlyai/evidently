import {
  SwitchViewMode,
  type TraceViewVariant
} from 'evidently-ui-lib/components/Traces/SwitchViewMode'
import { TraceToolbarRefContext } from 'evidently-ui-lib/contexts/TraceToolbarContext'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import { Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet, useParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useRef } from 'react'
import { useMatchRouter, useNavigate } from '~/routes/type-safe-route-helpers/hooks'
import type { GetParamsByPathAll } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces'
const exportIdRoutePath = `${currentRoutePath}/:exportId`

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'Traces' }
export const handle = { crumb }

///////////////////
//  COMPONENT
///////////////////
export const Component = () => {
  const params = useParams() as Partial<GetParamsByPathAll<typeof exportIdRoutePath>>

  const { projectId, exportId } = params

  const navigate = useNavigate()

  const traceToolbarRef = useRef<HTMLDivElement | null>(null)
  const viewMode = useViewMode()

  return (
    <>
      {viewMode && projectId && exportId && (
        <Stack my={2} direction={'row'} justifyItems={'center'} gap={2}>
          <Stack ref={traceToolbarRef} justifyContent={'center'} />
          <Stack flexGrow={1} direction={'row'} justifyContent={'flex-end'} pr={3}>
            <SwitchViewMode
              value={viewMode}
              onChange={(newMode) => {
                navigate({
                  to: `/projects/:projectId/traces/:exportId/${newMode}`,
                  paramsToReplace: { exportId, projectId }
                })
              }}
              isLoading={false}
            />
          </Stack>
        </Stack>
      )}

      <TraceToolbarRefContext.Provider value={traceToolbarRef}>
        <Outlet />
      </TraceToolbarRefContext.Provider>
    </>
  )
}

const useViewMode = (): TraceViewVariant | undefined => {
  const datasetMatch = useMatchRouter({ path: '/projects/:projectId/traces/:exportId/dataset' })
  const dialogMatch = useMatchRouter({ path: '/projects/:projectId/traces/:exportId/dialog' })
  const traceMatch = useMatchRouter({ path: '/projects/:projectId/traces/:exportId/trace' })

  const { viewMode } = {
    ...(datasetMatch && { viewMode: 'dataset' as const }),
    ...(dialogMatch && { viewMode: 'dialog' as const }),
    ...(traceMatch && { viewMode: 'trace' as const })
  }

  return viewMode
}
