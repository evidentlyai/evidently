import { RouteObject } from 'react-router'
import { redirect } from 'react-router-dom'

export default {
  path: 'test_suites/*',
  loader: ({ request }) =>
    redirect(request.url.replace('/test_suites', '/test-suites'), { status: 301 })
} satisfies RouteObject
