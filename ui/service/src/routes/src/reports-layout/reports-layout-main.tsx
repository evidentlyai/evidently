import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/reports'

const crumb: CrumbDefinition = { title: 'Reports' }

export const handle = { crumb }
