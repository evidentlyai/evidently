import { Box } from '@mui/material'
import type { PlotMouseEvent } from 'plotly.js'
import type React from 'react'
import { useState } from 'react'

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

  const OnClickComponent = viewParams?.OnClickedPointComponent
  const OnHoveredPlotComponent = viewParams?.OnHoveredPlotComponent

  const [clickEvent, setClickEvent] = useState<PlotMouseEvent | null>(null)
  const [isHovered, setIsHovered] = useState<boolean>(false)

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
    <>
      <Box position={'relative'}>
        <Plot
          onHover={() => !isHovered && setIsHovered(true)}
          onClick={OnClickComponent ? (e) => setClickEvent(e) : undefined}
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
        {clickEvent && OnClickComponent && <OnClickComponent event={clickEvent} />}
        {isHovered && OnHoveredPlotComponent && <OnHoveredPlotComponent />}
      </Box>
    </>
  )
}

export default BigGraphWidgetContent
