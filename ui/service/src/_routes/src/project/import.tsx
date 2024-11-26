export * as Project from '~/_routes/src/project/project-main'

const lazy = () => import('~/_routes/src/project/project-main')

export const ProjectLazy = { lazy } as const
