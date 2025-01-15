import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/test-suites'

const crumb: CrumbDefinition = { title: 'Test suites' }

export const handle = { crumb }
