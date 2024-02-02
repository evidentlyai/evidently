import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { redirect } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

export default {
  path: 'test_suites/*',
  loader: ({ request }) => redirect(request.url.replace('/test_suites', '/test-suites'))
} satisfies RouteObject
