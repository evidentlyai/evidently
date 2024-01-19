import React, { FunctionComponent } from 'react'
import { WidgetInfo } from '~/api'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

export interface DashboardContentProps {
  widgets: WidgetInfo[]
  ItemWrapper?: ({ id, children }: { id: string; children: React.ReactNode }) => React.ReactNode
}

export const DashboardContentWidgets: FunctionComponent<DashboardContentProps> = ({
  widgets,
  ItemWrapper
}) =>
  widgets.map((wi, idx) => (
    <React.Fragment key={wi.id}>{WidgetRenderer(`wi_${idx}`, wi, ItemWrapper)}</React.Fragment>
  ))
