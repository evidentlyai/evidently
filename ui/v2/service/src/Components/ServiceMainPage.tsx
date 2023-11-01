import React from 'react'
import { Box } from '@mui/material'
import { BreadCrumbs } from './BreadCrumbs'

export interface ServiceMainPageProps {
  children: React.ReactNode
}

export function ServiceMainPage(props: ServiceMainPageProps) {
  return (
    <>
      <Box sx={{ marginTop: '20px', marginLeft: '10px', marginRight: '10px', padding: '10px' }}>
        <BreadCrumbs />
        {props.children}
      </Box>
    </>
  )
}
