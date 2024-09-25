import { AppBar, Button, Link, Toolbar, Typography } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'
import { DiscordIcon } from '~/components/DiscordSvg'

export function ServiceHeader({
  version,
  authComponent,
  logoSrc
}: {
  authComponent?: React.ReactNode
  version: string
  logoSrc: string
}) {
  return (
    <>
      <AppBar position={'static'} sx={{ borderTop: 'none' }} color={'transparent'}>
        <Toolbar sx={{ gap: 1 }}>
          <Typography variant='h6' sx={{ flexGrow: 1 }}>
            <RouterLink to={'/'}>
              <img src={logoSrc} height='55px' alt='evidently logo' />
            </RouterLink>
            <span style={{ verticalAlign: 'super', fontSize: '0.75rem' }}>{version}</span>
          </Typography>

          {authComponent}

          <Button
            component={Link}
            startIcon={<DiscordIcon />}
            href={'https://discord.gg/tAHQeuDd'}
            target='_blank'
          >
            Support
          </Button>

          <Button component={Link} href={'https://docs.evidentlyai.com'} target='_blank'>
            Docs
          </Button>
        </Toolbar>
      </AppBar>
    </>
  )
}
