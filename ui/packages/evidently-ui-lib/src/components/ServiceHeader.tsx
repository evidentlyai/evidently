import { AppBar, Button, IconButton, Link, Toolbar, Typography } from '@mui/material'
import GitHubIcon from '@mui/icons-material/GitHub'
import axios from 'axios'

// openapi fetch



const handleReload = async () => {
  try {
    
    await axios.get('/api/projects/reload', {});
    // await openapiFetch.GET('/api/projects/reload'); // Replace 'your-api-endpoint' with the actual endpoint
    window.location.reload();
  } catch (error) {
    console.error('API call failed:', error);
  }
};

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
      <AppBar position={'static'} color={'transparent'}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            <img src={logoSrc} height="55px" />
            <span style={{ verticalAlign: 'super', fontSize: '0.75rem' }}>{version}</span>
          </Typography>
          {authComponent}
          <Link href={'https://github.com/evidentlyai/evidently'}>
            <IconButton>
              <GitHubIcon />
            </IconButton>
          </Link>
          <Link href={'https://docs.evidentlyai.com/'}>
            <Button>Docs</Button>
          </Link>
          <Button onClick={handleReload}>Reload</Button>
        </Toolbar>
      </AppBar>
    </>
  )
}
