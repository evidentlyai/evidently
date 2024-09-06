import type React from 'react'

import type { MultiTabGraphWidgetParams } from '~/api'

import AutoTabs from '~/components/AutoTabs'
import BigGraphWidgetContent from './BigGraphWidgetContent'

const TabbedGraphWidgetContent: React.FunctionComponent<
  MultiTabGraphWidgetParams & { widgetSize: number }
> = (props) => (
  <AutoTabs
    tabs={props.graphs.map((g) => ({
      title: g.title,
      tab: (
        <BigGraphWidgetContent
          widgetSize={props.widgetSize}
          data={g.graph.data}
          layout={g.graph.layout}
        />
      )
    }))}
  />
)

export default TabbedGraphWidgetContent
