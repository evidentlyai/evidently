///////////////////////////////
///  V2 TYPES
///////////////////////////////
import type { components, paths } from '~/api/types/endpoints_v2'

export type BackendPaths = paths

type Schemas = components['schemas']

type OmitNever<T> = { [K in keyof T as T[K] extends never ? never : K]: T[K] }

export type GetSearchParamsAPIs<T extends 'get' | 'post'> = OmitNever<{
  [P in keyof paths]: paths[P] extends Record<T, { parameters: { query?: infer Z } }> ? Z : never
}>

export type SeriesModel = Schemas['SeriesResponse']
export type BatchMetricDataModel = Schemas['BatchMetricData']
export type DashboardModel = Schemas['DashboardModel']
export type DashboardPanelPlotModel = Schemas['DashboardModel']['panels'][number]
