export * as Home from '~/_routes/src/home/home-main'

const lazy = () => import('~/_routes/src/home/home-main')

export const HomeLazy = { lazy } as const
