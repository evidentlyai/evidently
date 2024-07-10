import React from 'react'

import { AdditionalGraphInfo } from '~/api'
import Plot from '~/components/Plot'
import { useDashboardViewParams } from '~/contexts/DashboardViewParams'

interface BigGraphWidgetProps extends AdditionalGraphInfo {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  const viewParams = useDashboardViewParams()
  const isHistogram = props.data.some(({ type }) => type === 'histogram')

  return (
    <div>
      <Plot
        data={props.data}
        layout={{
          ...props.layout,
          title: undefined,
          xaxis: {
            ...props.layout?.xaxis,
            type: viewParams?.isXaxisAsCategorical && !isHistogram ? 'category' : undefined
          }
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
