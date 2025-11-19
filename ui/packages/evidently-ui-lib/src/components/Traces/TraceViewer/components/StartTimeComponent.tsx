import { Typography } from '@mui/material'
import type dayjs from 'dayjs'
import { InfoBlock } from './InfoBlock'

export const StartTimeComponent = ({ value }: { value: dayjs.Dayjs }) => (
  <InfoBlock title={'Start Time'}>
    <Typography>{value.locale('en-gb').format('lll')}</Typography>
  </InfoBlock>
)
