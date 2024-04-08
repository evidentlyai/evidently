import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/home/data'
import { api } from 'api/RemoteApi'
import logoSrc from 'assets/logo.png'

const { loader } = injectAPI({ api })

export default {
  path: '/',
  lazy: async () => {
    const { HomeComponentTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/home'
    )

    const Component = () => {
      return <HomeComponentTemplate logoSrc={logoSrc} />
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
