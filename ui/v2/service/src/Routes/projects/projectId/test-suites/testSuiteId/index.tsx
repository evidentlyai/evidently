import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui/routes-components/testSuiteId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  id: 'show-test-suite-by-id',
  path: ':testSuiteId',
  lazy: async () => {
    const { TestSuiteTemplate, ...rest } = await import(
      'evidently-ui/routes-components/testSuiteId'
    )

    const Component = () => {
      return <TestSuiteTemplate api={api} />
    }

    return { Component, ...rest }
  },
  loader
} satisfies RouteObject
