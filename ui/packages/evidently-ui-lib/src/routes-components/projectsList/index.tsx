import { Box, Grid, Typography } from '@mui/material'
import { loaderData } from './data'
import { useLoaderData } from 'react-router-dom'
import { ProjectCard } from '~/components/ProjectCard'
import React from 'react'

export const Component = () => {
  const projects = useLoaderData() as loaderData

  return (
    <>
      <Typography align="center" variant="h5">
        {projects.length > 0 ? 'Project List' : "You don't have any projects yet"}
      </Typography>
      <Box m="auto" mt={2} maxWidth={600}>
        <Grid container direction="column" justifyContent="center" alignItems="stretch">
          {projects.map((project) => (
            <React.Fragment key={project.id}>
              <ProjectCard project={project} />
            </React.Fragment>
          ))}
        </Grid>
      </Box>
    </>
  )
}
