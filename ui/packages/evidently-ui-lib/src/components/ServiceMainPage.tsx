import React from 'react'
import { Box } from '@mui/material'
import { BreadCrumbs } from './BreadCrumbs'

export interface ServiceMainPageProps {
  children: React.ReactNode
}

export function ServiceMainPage(props: ServiceMainPageProps) {
  return (
    <>
      <Box py={3}>
        <Box px={3}>
          <BreadCrumbs />
        </Box>
        {props.children}
      </Box>
    </>
  )
}
