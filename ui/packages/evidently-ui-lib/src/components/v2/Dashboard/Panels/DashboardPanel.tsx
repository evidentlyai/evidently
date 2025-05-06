import { assertNever } from '~/utils'
import { CounterDashboardPanel, type CounterPanelProps } from './implementations/Counter'
import { PieDashboardPanel, type PiePanelProps } from './implementations/Pie'
import { PlotDashboardPanel, type PlotPanelProps } from './implementations/Plot'
import { TextDashboardPanel, type TextPanelProps } from './implementations/Text'

export type DashboardPanelProps =
  | PlotPanelProps
  | CounterPanelProps
  | TextPanelProps
  | PiePanelProps

export const DashboardPanel = (props: DashboardPanelProps) => {
  if (props.type === 'bar' || props.type === 'line') {
    return <PlotDashboardPanel {...props} />
  }

  if (props.type === 'pie') {
    return <PieDashboardPanel {...props} />
  }

  if (props.type === 'counter') {
    return <CounterDashboardPanel {...props} />
  }

  if (props.type === 'text') {
    return <TextDashboardPanel {...props} />
  }

  assertNever(props.type)
}
