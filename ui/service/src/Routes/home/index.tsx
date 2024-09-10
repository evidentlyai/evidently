import { FetchersErrorSnackbar, GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { ReloadAllButton } from 'evidently-ui-lib/components/ReloadAllStateButton'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/home/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import logoSrc from '~/assets/logo.png'

const { loader, action } = getLoaderAction({ api: clientAPI })

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
          <HomeComponentTemplate
            logoSrc={logoSrc}
            reloadAllStateButton={<ReloadAllButton tooltipTitle='reload all state' action='/' />}
          />
        </>
      )
    }

    return { Component, ...rest }
  },
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
