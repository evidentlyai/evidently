import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'

///////////////////
//    ROUTE
///////////////////
export const currentRoutePath = '/projects/:projectId/prompts'

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'Prompts' }
export const handle = { crumb }
