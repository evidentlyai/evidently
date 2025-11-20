import { InfoOutlined as InfoIcon } from '@mui/icons-material'
import { Box, Tooltip, Typography } from '@mui/material'
import { CostTooltip } from './CostTooltip'
import { InfoBlock } from './InfoBlock'

export type CostComponentProps = {
  cost: number
  tokens: number
  breakdown: Map<string, [number, number]>
}

export const CostComponent = (props: CostComponentProps) => {
  const { cost, tokens } = props

  if (cost > 0) {
    return (
      <InfoBlock title={'Cost'}>
        <Box display={'flex'} alignItems={'center'} gap={0.5}>
          <Typography>${props.cost.toFixed(5)}</Typography>
          <Tooltip title={<CostTooltip {...props} />} slotProps={{ tooltip: { sx: { p: 0 } } }}>
            <InfoIcon fontSize='small' />
          </Tooltip>
        </Box>
      </InfoBlock>
    )
  }

  return (
    <InfoBlock title={'Tokens usage'}>
      <Box display={'flex'} alignItems={'center'} gap={0.5}>
        <Typography>{tokens} tokens</Typography>
        <Tooltip title={<CostTooltip {...props} />} slotProps={{ tooltip: { sx: { p: 0 } } }}>
          <InfoIcon fontSize='small' />
        </Tooltip>
      </Box>
    </InfoBlock>
  )
}
