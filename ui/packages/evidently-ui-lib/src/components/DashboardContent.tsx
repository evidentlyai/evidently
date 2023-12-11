import React, { FunctionComponent } from 'react'
import { WidgetInfo } from '~/api'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

export interface DashboardContentProps {
  widgets: WidgetInfo[]
}

export const DashboardContent: FunctionComponent<DashboardContentProps> = ({ widgets }) => (
  <React.Fragment>{widgets.map((wi, idx) => WidgetRenderer(`wi_${idx}`, wi))}</React.Fragment>
)
