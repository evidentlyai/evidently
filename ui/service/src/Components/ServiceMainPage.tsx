import React from 'react'
import { Paper } from '@material-ui/core'
import { BreadCrumbs } from './BreadCrumbs'

export interface ServiceMainPageProps {
  children: React.JSX.Element
}

export function ServiceMainPage(props: ServiceMainPageProps) {
  return (
    <>
      <Paper
        style={{ marginTop: '20px', marginLeft: '10px', marginRight: '10px', padding: '10px' }}
      >
        <BreadCrumbs />
        {props.children}
      </Paper>
    </>
  )
}
