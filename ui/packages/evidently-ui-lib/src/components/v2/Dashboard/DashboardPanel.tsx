import { assertNever } from '~/utils'
import { CounterDashboardPanel, type CounterPanelProps } from './Panels/Counter'
import { PlotDashboardPanel, type PlotPanelProps } from './Panels/Plot'
import { TextDashboardPanel, type TextPanelProps } from './Panels/Text'

export type DashboardPanelProps = PlotPanelProps | CounterPanelProps | TextPanelProps

export const DashboardPanel = (props: DashboardPanelProps) => {
  if (props.plotType === 'bar' || props.plotType === 'line') {
    return <PlotDashboardPanel {...props} />
  }

  if (props.plotType === 'counter') {
    return <CounterDashboardPanel {...props} />
  }

  if (props.plotType === 'text') {
    return <TextDashboardPanel {...props} />
  }

  assertNever(props.plotType)
}
