import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/reportId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  id: 'show-report-by-id',
  path: ':reportId',
  lazy: async () => {
    const { ReportTemplate, ...rest } = await import('evidently-ui-lib/routes-components/reportId')

    const Component = () => {
      return <ReportTemplate api={api} />
    }

    return { Component, ...rest }
  },
  loader
} satisfies RouteObject
