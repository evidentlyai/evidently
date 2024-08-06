import type React from 'react'

import type { MultiTabWidgetParams } from '~/api'

import AutoTabs from '~/components/AutoTabs'
import { WidgetRenderer } from './WidgetRenderer'

const TabbedWidgetContent: React.FunctionComponent<
  MultiTabWidgetParams & { id: string; widgetSize: number }
> = (props) => {
  return (
    <AutoTabs
      tabs={props.tabs.map((g) => ({
        title: g.title,
        tab: WidgetRenderer(`${props.id}1`, g.widget)
      }))}
    />
  )
}

export default TabbedWidgetContent
