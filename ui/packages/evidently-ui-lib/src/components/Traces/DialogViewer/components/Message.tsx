import { Paper, Stack, Typography } from '@mui/material'

type MessageProps = {
  title: string
  message: string
  time: string
  align: 'left' | 'right'
}

export const Message = (props: MessageProps) => {
  const { title, message, time, align } = props

  return (
    <Paper
      sx={(theme) => ({
        p: 2,
        border: 'none',
        borderRadius: 4,
        marginLeft: align === 'right' ? 3 : '0',
        marginRight: align === 'right' ? '0' : 3,
        ...theme.applyStyles('light', {
          bgcolor: '#f6f6f6'
        })
      })}
    >
      <Stack gap={1}>
        <Typography
          align={align}
          variant={'caption'}
          fontWeight={'bold'}
          fontSize={'1.1rem'}
          component='pre'
          sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces' }}
        >
          {title}
        </Typography>
        <Typography
          align={'left'}
          fontSize={'1rem'}
          component='pre'
          sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces' }}
        >
          {message?.trim()}
        </Typography>

        <Typography
          align={align === 'right' ? 'left' : 'right'}
          fontSize={'0.875rem'}
          component='pre'
          sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces' }}
        >
          {time}
        </Typography>
      </Stack>
    </Paper>
  )
}
