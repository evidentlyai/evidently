import React from 'react'

import { Api, AdditionalGraphInfo, WidgetInfo } from '~/api'
import { DashboardInfoModel } from '~/api/types'

interface ApiContextState {
  Api: Api
}

class NotImplementedApi implements Api {
  getAdditionalGraphData(): Promise<AdditionalGraphInfo> {
    return Promise.reject('not implemented')
  }

  getAdditionalWidgetData(): Promise<WidgetInfo> {
    return Promise.reject('not implemented')
  }

  getDashboard(): Promise<DashboardInfoModel> {
    return Promise.reject('not implemented')
  }
}

const ApiContext = React.createContext<ApiContextState>({ Api: new NotImplementedApi() })

export default ApiContext
