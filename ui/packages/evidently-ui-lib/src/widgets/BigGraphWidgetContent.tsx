import { Box } from '@mui/material'
import type React from 'react'
import type { AdditionalGraphInfo } from '~/api'
import Plot, { darkPlotlyLayoutTemplate } from '~/components/Plots/Plot'
import { useThemeMode } from '~/hooks/theme'

interface BigGraphWidgetProps extends AdditionalGraphInfo {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  const mode = useThemeMode()

  const shapes = [...(props.layout.shapes ?? [])]

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

  return (
    <>
      <Box position={'relative'}>
        <Plot
          data={props.data}
          layout={{ ...props.layout, ...tOverride, title: undefined, shapes }}
          config={{ responsive: true }}
          style={{
            width: '100%',
            minHeight: 300 + 100 * (1 + props.widgetSize / 2),
            maxHeight: 400
          }}
        />
      </Box>
    </>
  )
}

export default BigGraphWidgetContent
