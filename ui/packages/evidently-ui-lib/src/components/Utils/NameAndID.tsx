import { Stack, Typography } from '@mui/material'
import { TextWithCopyIcon } from './TextWithCopyIcon'

type NameAndIDProps = { name: string; id: string }

export const NameAndID = ({ name, id }: NameAndIDProps) => {
  const isOnlyID = id && !name

  if (isOnlyID) {
    return (
      <Typography color={'text.secondary'} variant={'subtitle2'}>
        <TextWithCopyIcon showText={id} copyText={id} tooltip={'Copy ID'} />
      </Typography>
    )
  }

  return (
    <Stack direction={'column'}>
      <Typography variant={'subtitle2'}>{name}</Typography>
      <Typography
        component={'div'}
        fontSize={'xx-small'}
        fontFamily={'monospace'}
        color={'text.secondary'}
      >
        <TextWithCopyIcon showText={id} copyText={id} tooltip={'Copy ID'} />
      </Typography>
    </Stack>
  )
}
