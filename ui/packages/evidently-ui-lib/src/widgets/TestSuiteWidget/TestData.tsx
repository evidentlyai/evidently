import { Alert, type AlertColor, AlertTitle, Box, Button, Collapse } from '@mui/material'
import type React from 'react'
import { useState } from 'react'
import type { TestDataInfo, TestState } from '~/api'

import ReactMarkdown from 'react-markdown'
import { BigTableDetails } from '~/widgets/BigTableWidget/BigTableDetails'

const availableStates: TestState[] = ['unknown', 'success', 'warning', 'fail']

export const StateToSeverity: (state: TestState) => AlertColor = (state) => {
  switch (state) {
    case 'error':
    case 'unknown':
      return 'info'
    case 'success':
      return 'success'
    case 'warning':
      return 'warning'
    case 'fail':
      return 'error'
  }
}

const TestData: React.FC<TestDataInfo> = ({ title, description, state, details }) => {
  const [detailsPart, setDetailsPart] = useState({ active: false })
  const isDetailsAvailable = details !== undefined && details !== null && details.parts.length > 0
  if (!availableStates.includes(state)) {
    console.error(`unexpected state: ${state} (expected one of [${availableStates.join(', ')}])`)
    state = 'unknown'
  }
  return (
    <>
      <Box>
        <Alert
          severity={StateToSeverity(state)}
          action={
            isDetailsAvailable ? (
              <Button
                onClick={() => setDetailsPart((prev) => ({ active: !prev.active }))}
                color='inherit'
                size='small'
              >
                Details
              </Button>
            ) : null
          }
        >
          <AlertTitle>{title}</AlertTitle>
          <ReactMarkdown>{description}</ReactMarkdown>
        </Alert>
        {!isDetailsAvailable ? (
          <></>
        ) : (
          <Collapse in={detailsPart.active} mountOnEnter={true} unmountOnExit={true}>
            <Box style={{ padding: '2px' }}>
              <BigTableDetails details={details} widgetSize={2} />
            </Box>
          </Collapse>
        )}
      </Box>
    </>
  )
}

export default TestData
