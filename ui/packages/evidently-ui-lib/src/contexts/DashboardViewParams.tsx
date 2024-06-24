import React, { useContext } from 'react'

export type DashboardViewParams = {
  isXaxisAsCategorical: boolean
} | null

export const DashboardViewParamsContext = React.createContext<DashboardViewParams>(null)

export const useDashboardViewParams = () => useContext(DashboardViewParamsContext)
