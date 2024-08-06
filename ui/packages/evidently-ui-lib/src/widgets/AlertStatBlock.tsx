import type React from 'react'

import { Typography } from '@mui/material'
import type { AlertStats } from '~/api'
import AlertBlock from './AlertBlock'

interface AlertStatBlockProps {
  alertStats: AlertStats
}

const AlertStatBlock: React.FunctionComponent<AlertStatBlockProps> = (props) => {
  const { alertStats } = props
  return (
    <AlertBlock
      data={{
        value: `${alertStats.triggered.last_24h}`,
        state: 'info',
        text: 'alerts in the last 24 hours',
        longText: 'alerts triggered in the period / alerts triggered in 24 hours / alerts active '
      }}
      customPopup={
        <Typography sx={{ pr: 1 }}>
          <ul>
            <li>{alertStats.triggered.period} alerts triggered in the period</li>
            <li>{alertStats.triggered.last_24h} alerts triggered in 24 hours</li>
            <li>{alertStats.active} total active alerts</li>
          </ul>
        </Typography>
      }
    />
  )
}

export default AlertStatBlock
