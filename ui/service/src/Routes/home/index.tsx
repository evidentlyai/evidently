import { FetchersErrorSnackbar, GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { EvidentlyLogoSvg } from 'evidently-ui-lib/components/LogoSvg'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/home/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'

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
          <HomeComponentTemplate LogoSvg={EvidentlyLogoSvg} />
        </>
      )
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
