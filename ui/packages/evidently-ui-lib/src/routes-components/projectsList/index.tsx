import { Box, Grid, Typography } from '@mui/material'
import React from 'react'
import { useLoaderData } from 'react-router-dom'
import { AddNewProjectButton, ProjectCard } from '~/components/ProjectCard'
import type { LoaderData } from './data'

export const Component = () => {
  const projects = useLoaderData() as LoaderData

  return (
    <>
      <Typography align='center' variant='h5'>
        {projects.length > 0 ? 'Project List' : "You don't have any projects yet"}
      </Typography>
      <Box m='auto' mt={2} maxWidth={600}>
        <AddNewProjectButton />
        <Grid container direction='column' justifyContent='center' alignItems='stretch'>
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
