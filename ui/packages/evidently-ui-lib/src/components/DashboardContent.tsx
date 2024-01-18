import React, { FunctionComponent } from 'react'
import { WidgetInfo } from '~/api'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

export interface DashboardContentProps {
  widgets: WidgetInfo[]
}

export const DashboardContentWidgets: FunctionComponent<DashboardContentProps> = ({ widgets }) =>
  widgets.map((wi, idx) => (
    <React.Fragment key={wi.id}>{WidgetRenderer(`wi_${idx}`, wi)}</React.Fragment>
  ))
