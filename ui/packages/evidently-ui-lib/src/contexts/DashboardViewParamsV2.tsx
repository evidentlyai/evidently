import React, { useContext } from 'react'

export type DashboardViewParams = {
  isXaxisAsCategorical: boolean
  OnClickedPointComponent?: (data: { snapshotId: string }) => JSX.Element
} | null

export const DashboardViewParamsContext = React.createContext<DashboardViewParams>(null)

export const useDashboardViewParams = () => useContext(DashboardViewParamsContext)
