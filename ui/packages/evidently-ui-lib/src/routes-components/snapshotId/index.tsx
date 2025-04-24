import { Box } from '@mui/material'
import type { DashboardInfoModel } from '~/api/types'
import { SnapshotWidgets } from '~/components/WidgetsContent'
import DashboardContext, {
  CreateDashboardContextState,
  type DashboardContextState
} from '~/contexts/DashboardContext'

export const SnapshotTemplateComponent = ({
  data,
  dashboardContextState
}: {
  dashboardContextState: DashboardContextState
  data: DashboardInfoModel
}) => {
  return (
    <>
      <DashboardContext.Provider value={CreateDashboardContextState(dashboardContextState)}>
        <Box py={2}>
          <SnapshotWidgets widgets={data.widgets} />
        </Box>
      </DashboardContext.Provider>
    </>
  )
}
