// export * as Dashboard from './dashboard-main'

// we export it lazy because of ~2.6 MB chunk size :) plotly.js is too big :3
const lazy = () => import('./dashboard-main')
export const DashboardLazy = { lazy } as const
