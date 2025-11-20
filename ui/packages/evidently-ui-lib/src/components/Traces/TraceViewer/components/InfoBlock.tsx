import { Stack, Typography } from '@mui/material'
import type { ReactElement } from 'react'

type InfoBlockProps = {
  title: string
  children: ReactElement
}

export const InfoBlock = (props: InfoBlockProps) => {
  const { title, children } = props

  return (
    <Stack maxWidth={'sm'} direction='column' spacing={1}>
      <Typography variant={'subtitle2'}>{title}</Typography>
      {children}
    </Stack>
  )
}
