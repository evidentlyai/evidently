import React, { useEffect, useState } from 'react'
import { Box } from '@mui/material'
import { useParams } from 'react-router-dom'
import { SideBar, SideBarLink } from '~/components/Sidebar'

export interface ServiceMainPageProps {
  children: React.ReactNode
  additionalProjectSideBarLinks?: SideBarLink[]
}

export function ServiceMainPage({
  children,
  additionalProjectSideBarLinks = []
}: ServiceMainPageProps) {
  const { projectId } = useParams()
  const [sideBarSize, setSideBarSize] = useState(projectId ? 65 : 0)

  useEffect(() => {
    if (projectId) {
      setSideBarSize(65)
    } else {
      setSideBarSize(0)
    }
  }, [projectId])

  return (
    <Box
      display={'grid'}
      gridTemplateColumns={`${sideBarSize}px 1px calc(100% - ${sideBarSize}px - 1px)`}
      alignItems={'start'}
      sx={{ transition: '225ms ease-in-out' }}
    >
      <Box sx={{ position: 'sticky', top: 0, left: 0, overflow: 'hidden' }}>
        <SideBar projectId={projectId} additionalLinks={additionalProjectSideBarLinks} />
      </Box>
      <Box sx={{ height: 1, backgroundColor: 'primary.light' }}></Box>
      <Box>{children}</Box>
    </Box>
  )
}
