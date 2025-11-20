import { InfoOutlined as InfoIcon } from '@mui/icons-material'
import { Box, Tooltip, Typography } from '@mui/material'
import type { TraceModel } from 'api/types'
import { ExtractUsageData } from '../helpers'
import { CostTooltip } from './CostTooltip'

type UsageDataProps = { trace: TraceModel }

export const UsageData = (props: UsageDataProps) => {
  const { trace } = props

  const extractUsageData = ExtractUsageData(trace)
  const totalTokens = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][0], 0)
  const totalCost = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][1], 0)

  return (
    <Box display={'flex'} alignItems={'center'} gap={0.5}>
      {totalCost > 0 ? (
        <Typography>${totalCost.toFixed(5)}</Typography>
      ) : (
        <Typography>{totalTokens} tokens</Typography>
      )}

      <Tooltip
        title={<CostTooltip breakdown={extractUsageData} cost={totalCost} tokens={totalTokens} />}
        slotProps={{ tooltip: { sx: { p: 0 } } }}
      >
        <InfoIcon fontSize='small' />
      </Tooltip>
    </Box>
  )
}
