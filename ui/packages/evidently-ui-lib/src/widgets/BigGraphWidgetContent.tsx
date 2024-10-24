import type React from 'react'

import type { AdditionalGraphInfo } from '~/api'
import Plot, { darkPlotlyLayoutTemplate } from '~/components/Plot'
import { useDashboardViewParams } from '~/contexts/DashboardViewParams'
import { useThemeMode } from '~/hooks/theme'

interface BigGraphWidgetProps extends AdditionalGraphInfo {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  const viewParams = useDashboardViewParams()
  const mode = useThemeMode()
  const isHistogram = props.data.some(({ type }) => type === 'histogram')
  const isCastXaxisToCategory = viewParams?.isXaxisAsCategorical && !isHistogram

  const tOverride =
    mode === 'dark'
      ? {
          template: {
            ...darkPlotlyLayoutTemplate,
            layout: {
              ...darkPlotlyLayoutTemplate.layout,
              colorway:
                props.layout.template?.layout?.colorway || darkPlotlyLayoutTemplate.layout?.colorway
            }
          }
        }
      : undefined
  const xaxisOptionsOverride = isCastXaxisToCategory
    ? ({ type: 'category', categoryorder: 'category ascending' } as const)
    : undefined

  return (
    <div>
      <Plot
        data={props.data}
        layout={{
          ...props.layout,
          ...tOverride,
          title: undefined,
          xaxis: { ...props.layout?.xaxis, ...xaxisOptionsOverride }
        }}
        config={{ responsive: true }}
        style={{
          width: '100%',
          minHeight: 300 + 100 * (1 + props.widgetSize / 2),
          maxHeight: 400
        }}
      />
    </div>
  )
}

export default BigGraphWidgetContent
