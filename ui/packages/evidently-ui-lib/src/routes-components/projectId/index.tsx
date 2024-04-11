import { Box, Grid, IconButton, Typography } from '@mui/material'

import { Outlet, useLoaderData } from 'react-router-dom'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'

import { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.name || 'undefined' })
}

export const ProjectTemplate = () => {
  const project = useLoaderData() as loaderData

  return (
    <Box mt={1}>
      <Grid container spacing={2} direction="row" justifyContent="flex-start" alignItems="flex-end">
        <Grid item xs={12}>
          <Typography sx={{ color: '#aaa' }} variant="body2">
            {`project id: ${project.id}`}
            <IconButton
              size="small"
              style={{ marginLeft: 10 }}
              onClick={() => navigator.clipboard.writeText(project.id)}
            >
              <ContentCopyIcon fontSize="small" />
            </IconButton>
          </Typography>
        </Grid>
      </Grid>
      <Outlet />
    </Box>
  )
}

export const Component = ProjectTemplate
