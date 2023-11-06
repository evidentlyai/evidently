import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/home/data'
import { api } from 'api/RemoteApi'

import { theme } from 'evidently-ui-lib/theme/v1'
import logoSrc from 'assets/logo.png'

const { loader } = injectAPI({ api })

export default {
  path: '/',
  lazy: async () => {
    const { HomeComponentTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/home'
    )

    const Component = () => {
      return <HomeComponentTemplate theme={theme} logoSrc={logoSrc} />
    }

    return { Component, ...rest }
  },
  loader
} satisfies RouteObject
