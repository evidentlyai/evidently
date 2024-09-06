import type React from 'react'

import { Box } from '@mui/material'

import type {
  AdditionalGraphInfo,
  BigTableRowDetails,
  DetailsPart,
  WidgetInfo,
  WidgetSize
} from '~/api'

import DashboardContext, { type DashboardContextState } from '~/contexts/DashboardContext'

import AutoTabs from '~/components/AutoTabs'
import LoadableView from '~/components/LoadableVIew'

import BigGraphWidgetContent from '~/widgets/BigGraphWidgetContent'
import InsightBlock from '~/widgets/InsightBlock'
import NotImplementedWidgetContent from '~/widgets/NotImplementedWidgetContent'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

interface BigTableDetailsProps {
  details: BigTableRowDetails
  widgetSize: WidgetSize
}

const GetType = (part: DetailsPart) => part.type ?? 'graph'

const RenderPart = (context: DashboardContextState, part: DetailsPart, widgetSize: number) => {
  switch (GetType(part)) {
    case 'graph': {
      const get = () => context.getAdditionGraphData(part.id)
      const render = (params: AdditionalGraphInfo) => (
        <BigGraphWidgetContent {...params} widgetSize={widgetSize} />
      )
      return <LoadableView func={get}>{render}</LoadableView>
    }
    case 'widget': {
      const get = () => context.getAdditionWidgetData(part.id)
      const render = (params: WidgetInfo) => WidgetRenderer(part.id, params)
      return <LoadableView func={get}>{render}</LoadableView>
    }
    default:
      return <NotImplementedWidgetContent />
  }
}

export const BigTableDetails: React.FunctionComponent<BigTableDetailsProps> = (props) => {
  return (
    <DashboardContext.Consumer>
      {(dashboardContext) => (
        <Box>
          {props.details.parts.length > 1 ? (
            <AutoTabs
              tabs={props.details.parts.map((part) => ({
                title: part.title,
                tab: RenderPart(dashboardContext, part, props.widgetSize)
              }))}
            />
          ) : (
            RenderPart(dashboardContext, props.details.parts[0], props.widgetSize)
          )}
          {props.details.insights === undefined ? (
            <></>
          ) : (
            props.details.insights.map((row) => (
              <InsightBlock key={row.text + row.title + row.severity} data={row} />
            ))
          )}
        </Box>
      )}
    </DashboardContext.Consumer>
  )
}
