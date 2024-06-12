import React from 'react'

import { AdditionalGraphInfo } from '~/api'
import Plot from '~/components/Plot'

interface BigGraphWidgetProps extends AdditionalGraphInfo {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  return (
    <div>
      <Plot
        data={props.data}
        layout={{
          ...props.layout,
          title: undefined
          // width: (props.size.width ? props.size.width - 20 : undefined)
        }}
        config={{ responsive: true }}
        style={{ width: '100%', minHeight: 300 + 100 * (1 + props.widgetSize / 2), maxHeight: 400 }}
      />
    </div>
  )
}

export default BigGraphWidgetContent
