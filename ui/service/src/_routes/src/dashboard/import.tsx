// export * as Dashboard from '~/_routes/src/dashboard/dashboard-main'

const lazy = () => import('~/_routes/src/dashboard/dashboard-main')
export const Dashboard = { lazy } as const
