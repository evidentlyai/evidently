import React from 'react'

import { BigGraphWidgetParams } from '~/api'
import Plot from '~/components/Plot'

interface BigGraphWidgetProps extends BigGraphWidgetParams {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  return (
    <div>
      <Plot
        data={props.data}
        layout={{
          ...props.layout,
          title: undefined,
          font: { size: 20 },
          legend: {
            xanchor: 'right',
            x: 1,
            y: 1,
            bgcolor: '#ebebeb'
          },
          paper_bgcolor: 'white',
          plot_bgcolor: 'white'
          // width: (props.size.width ? props.size.width - 20 : undefined)
        }}
        config={{ responsive: true }}
        style={{ width: '100%', minHeight: 300 + 100 * (1 + props.widgetSize / 2), maxHeight: 400 }}
      />
    </div>
  )
}

export default BigGraphWidgetContent
