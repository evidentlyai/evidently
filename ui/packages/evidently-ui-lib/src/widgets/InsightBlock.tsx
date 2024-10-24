import type React from 'react'

import { AlertTitle } from '@mui/material'

import type { InsightsParams } from '~/api'
import { AlertThemed } from '~/components/AlertThemed'

interface InsightBlockProps {
  data: InsightsParams
}

const InsightBlock: React.FunctionComponent<InsightBlockProps> = (props) => {
  return (
    <AlertThemed severity={props.data.severity}>
      <AlertTitle>{props.data.title}</AlertTitle>
      {props.data.text}
    </AlertThemed>
  )
}

export default InsightBlock
