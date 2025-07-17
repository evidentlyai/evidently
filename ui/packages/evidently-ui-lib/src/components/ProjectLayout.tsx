import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { Box, Grid, IconButton, Typography } from '@mui/material'
import type { ProjectModel } from '~/api/types'
import type { StrictID } from '~/api/types/utils'

const ProjectInfoLayout = ({ project }: { project: StrictID<ProjectModel> }) => {
  return (
    <Grid container spacing={2} direction='row' justifyContent='flex-start' alignItems='flex-end'>
      <Grid size={{ xs: 12 }}>
        <Typography color='text.secondary' variant='body2'>
          project id: {project.id}
          <IconButton
            size='small'
            style={{ marginLeft: 10 }}
            onClick={() => {
              navigator.clipboard.writeText(project.id)
            }}
          >
            <ContentCopyIcon fontSize='small' />
          </IconButton>
        </Typography>
      </Grid>
    </Grid>
  )
}

export const ProjectLayoutTemplate = ({
  project,
  children
}: {
  project: StrictID<ProjectModel>
  children?: React.ReactNode
}) => {
  return (
    <Box mt={2}>
      <ProjectInfoLayout project={project} />

      {children}
    </Box>
  )
}
