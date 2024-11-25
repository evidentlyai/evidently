export * as Home from '~/_routes/src/home/home'

export const HomeLazy = { lazy: () => import('~/_routes/src/home/home') } as const
