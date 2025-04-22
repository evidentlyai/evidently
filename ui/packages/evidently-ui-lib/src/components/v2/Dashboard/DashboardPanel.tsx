import { assertNever } from '~/utils'
import { CustomDashboardPanel, type CustomPanelProps } from './Panels/CustomDashboardPanel'
import { PlotDashboardPanel, type PlotPanelProps } from './Panels/DashboardPanel'

export type DashboardPanelProps = PlotPanelProps | CustomPanelProps

export const DashboardPanel = (props: DashboardPanelProps) => {
  if (props.plotType === 'bar' || props.plotType === 'line') {
    return <PlotDashboardPanel {...props} />
  }

  if (props.plotType === 'counter' || props.plotType === 'text') {
    return <CustomDashboardPanel {...props} />
  }

  assertNever(props.plotType)
}
