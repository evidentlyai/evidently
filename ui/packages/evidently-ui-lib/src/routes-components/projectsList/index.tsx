import { Typography } from '@mui/material'
import { useLoaderData } from 'react-router-dom'

import type { LoaderData } from './data'

export const Component = () => {
  const projects = useLoaderData() as LoaderData

  return (
    <>
      <Typography align='center' variant='h5'>
        {projects.length > 0 ? 'Project List' : "You don't have any projects yet"}
      </Typography>
    </>
  )
}
