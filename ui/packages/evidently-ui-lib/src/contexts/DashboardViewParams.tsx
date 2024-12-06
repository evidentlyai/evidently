import type { PlotMouseEvent } from 'plotly.js'
import React, { useContext } from 'react'

export type DashboardViewParams = {
  isXaxisAsCategorical: boolean
  OnClickedPointComponent?: ({ event }: { event: PlotMouseEvent }) => JSX.Element
  OnHoveredPlotComponent?: () => JSX.Element
} | null

export const DashboardViewParamsContext = React.createContext<DashboardViewParams>(null)

export const useDashboardViewParams = () => useContext(DashboardViewParamsContext)
