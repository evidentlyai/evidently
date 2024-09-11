import type React from 'react'

import { Alert, AlertTitle } from '@mui/material'

import type { InsightsParams } from '~/api'

interface InsightBlockProps {
  data: InsightsParams
}

const InsightBlock: React.FunctionComponent<InsightBlockProps> = (props) => {
  return (
    <Alert severity={props.data.severity}>
      <AlertTitle>{props.data.title}</AlertTitle>
      {props.data.text}
    </Alert>
  )
}

export default InsightBlock
