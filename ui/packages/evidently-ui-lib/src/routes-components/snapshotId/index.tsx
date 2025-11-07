import { Box } from '@mui/material'
import type { DashboardInfoModel } from '~/api/types'
import { SnapshotWidgets } from '~/components/Widgets/WidgetsContent'
import DashboardContext, {
  CreateDashboardContextState,
  type DashboardContextState
} from '~/contexts/DashboardContext'

type SnapshotTemplateComponentProps = {
  dashboardContextState: DashboardContextState
  data: DashboardInfoModel
}
export const SnapshotTemplateComponent = (props: SnapshotTemplateComponentProps) => {
  const { data, dashboardContextState } = props

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
