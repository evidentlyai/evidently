export * as ProjectsList from '~/_routes/src/projects-list/projects-list-main'

const lazy = () => import('~/_routes/src/projects-list/projects-list-main')

export const ProjectsListLazy = { lazy } as const
