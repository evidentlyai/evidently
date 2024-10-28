import { AppBar, Button, IconButton, Link, Stack, Toolbar } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'
import { DiscordIcon } from '~/components/DiscordSvg'
import { ThemeToggle } from '~/components/ThemeToggle'

export function ServiceHeader({
  LogoSvg,
  version,
  authComponent
}: {
  LogoSvg: () => JSX.Element
  authComponent?: React.ReactNode
  version: string
}) {
  return (
    <>
      <AppBar
        position={'static'}
        sx={{
          borderLeft: 'none',
          borderRight: 'none',
          borderTop: 'none',
          borderBottom: '1px solid',
          borderColor: (t) => t.palette.divider
        }}
        color={'transparent'}
      >
        <Toolbar sx={{ gap: 1 }}>
          <Stack flexGrow={1} justifyContent={'flex-start'} direction={'row'}>
            <Stack direction={'row'} alignItems={'flex-end'} gap={1}>
              <IconButton
                component={RouterLink}
                to={'/'}
                sx={(theme) => ({
                  color: '#4d4d4d',
                  ...theme.applyStyles('dark', {
                    color: theme.palette.text.primary
                  }),
                  '&:hover': {
                    borderRadius: '5px',
                    color: theme.palette.text.disabled,
                    ...theme.applyStyles('dark', {
                      color: theme.palette.text.secondary
                    })
                  }
                })}
              >
                <LogoSvg />
              </IconButton>
              <span style={{ verticalAlign: 'super', fontSize: '0.75rem' }}>{version}</span>
            </Stack>
          </Stack>

          {authComponent}

          <Button
            component={Link}
            startIcon={<DiscordIcon />}
            href='https://discord.gg/EJxU68uynY'
            target='_blank'
          >
            Support
          </Button>

          <Button component={Link} href='https://docs.evidentlyai.com' target='_blank'>
            Docs
          </Button>

          <ThemeToggle />
        </Toolbar>
      </AppBar>
    </>
  )
}
