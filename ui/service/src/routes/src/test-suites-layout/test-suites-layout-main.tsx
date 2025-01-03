import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/test-suites'

const crumb: CrumbDefinition = { title: 'Test suites' }

export const handle = { crumb }
