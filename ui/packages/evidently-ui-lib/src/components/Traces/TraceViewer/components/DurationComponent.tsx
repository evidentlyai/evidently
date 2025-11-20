import { Typography } from '@mui/material'
import { InfoBlock } from './InfoBlock'

type DurationComponentProps = {
  value: number
}

export const DurationComponent = (props: DurationComponentProps) => {
  const { value } = props

  return (
    <InfoBlock title={'Duration'}>
      <Typography>{value > 1000 ? `${(value / 1000).toFixed(1)} s` : `${value} ms`}</Typography>
    </InfoBlock>
  )
}
