export * as ProjectsList from '~/_routes/src/projectsList/projectsList'

export const ProjectsListLazy = {
  lazy: () => import('~/_routes/src/projectsList/projectsList')
} as const
