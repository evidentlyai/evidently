import React from 'react'
import { Paper } from '@mui/material'
import { BreadCrumbs } from './BreadCrumbs'

export interface ServiceMainPageProps {
  children: React.ReactNode
}

export function ServiceMainPage(props: ServiceMainPageProps) {
  return (
    <>
      <Paper sx={{ marginTop: '20px', marginLeft: '10px', marginRight: '10px', padding: '10px' }}>
        <BreadCrumbs />
        {props.children}
      </Paper>
    </>
  )
}
