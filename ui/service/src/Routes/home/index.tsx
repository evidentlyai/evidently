import { FetchersErrorSnackbar, GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/home/data'
import { clientAPI } from '~/api'
import logoSrc from '~/assets/logo.png'

const { loader } = getLoaderAction({ api: clientAPI })

export default {
  path: '/',
  lazy: async () => {
    const { HomeComponentTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/home'
    )

    const Component = () => {
      return (
        <>
          <FetchersErrorSnackbar />
          <HomeComponentTemplate logoSrc={logoSrc} />
        </>
      )
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
