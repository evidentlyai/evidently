import { Box, Card, Chip, Stack, Typography } from '@mui/material'
import { TextWithCopyIcon } from '~/components/Utils/TextWithCopyIcon'

type PromptProps = {
  text: string
  role?: string
}

export const Prompt = (props: PromptProps) => {
  const { text, role } = props

  return (
    <Box position={'relative'}>
      <Box position={'absolute'} top={5} right={5}>
        <TextWithCopyIcon showText={''} copyText={text} />
      </Box>

      {role && (
        <Box position={'absolute'} top={10} left={15}>
          <Stack direction={'row'} alignItems={'center'} gap={1}>
            <Typography variant='body2' fontFamily={'monospace'}>
              Role:
            </Typography>
            <Chip size='small' label={role} sx={{ fontFamily: 'monospace' }} />
          </Stack>
        </Box>
      )}

      <Card sx={[{ p: 5 }, !!role && { pt: 8 }]}>
        <Typography
          component='pre'
          sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces', fontSize: '1rem' }}
        >
          {text}
        </Typography>
      </Card>
    </Box>
  )
}
