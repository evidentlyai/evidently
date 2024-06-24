import React from 'react'

import { BigGraphWidgetParams } from '~/api'
import Plot from '~/components/Plot'
import { useDashboardViewParams } from '~/contexts/DashboardViewParams'

interface BigGraphWidgetProps extends BigGraphWidgetParams {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  const viewParams = useDashboardViewParams()

  return (
    <div>
      <Plot
        data={props.data}
        layout={{
          ...props.layout,
          title: undefined,
          xaxis: {
            ...props.layout?.xaxis,
            type: viewParams?.isXaxisAsCategorical ? 'category' : undefined
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
