import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

///////////////////
//    ROUTE
///////////////////

export const _route_path = '/:projectId/test-suites'

const crumb: CrumbDefinition = { title: 'Test suites' }

export const handle = { crumb }
