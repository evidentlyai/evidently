import React, { useContext } from 'react'

export type DashboardViewParams = {
  OnClickedPointComponent?: (data: { snapshotId: string }) => JSX.Element
} | null

export const DashboardViewParamsContext = React.createContext<DashboardViewParams>(null)

export const useDashboardViewParams = () => useContext(DashboardViewParamsContext)
