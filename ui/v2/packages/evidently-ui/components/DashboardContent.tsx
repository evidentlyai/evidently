import React, { FunctionComponent } from 'react'
import { DashboardInfo } from '../api'
import { WidgetRenderer } from '../widgets/WidgetRenderer'

export interface DashboardContentProps {
  info: DashboardInfo
}

export const DashboardContent: FunctionComponent<DashboardContentProps> = (props) => (
  <React.Fragment>
    {props.info.widgets.map((wi, idx) => WidgetRenderer(`wi_${idx}`, wi))}
  </React.Fragment>
)
