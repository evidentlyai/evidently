import React from 'react'
import { Box } from '@mui/material'
import { BreadCrumbs } from './BreadCrumbs'

export interface ServiceMainPageProps {
  children: React.ReactNode
}

export function ServiceMainPage(props: ServiceMainPageProps) {
  return (
    <>
      <Box p={3}>
        <BreadCrumbs />
        {props.children}
      </Box>
    </>
  )
}
