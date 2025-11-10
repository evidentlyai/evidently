import type React from 'react'

import type { MultiTabWidgetParams } from '~/api'

import AutoTabs from '~/components/Tabs/AutoTabs'
import { WidgetRenderer } from './WidgetRenderer'

const TabbedWidgetContent: React.FunctionComponent<
  MultiTabWidgetParams & { id: string; widgetSize: number }
> = (props) => {
  return (
    <AutoTabs
      tabs={props.tabs.map((g) => ({
        title: g.title,
        tab: <WidgetRenderer info={g.widget} />
      }))}
    />
  )
}

export default TabbedWidgetContent
