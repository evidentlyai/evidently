import React, { useEffect, useState } from 'react'
import { Box, Divider } from '@mui/material'
import { useParams } from 'react-router-dom'
import { SideBar, SideBarLink } from '~/components/Sidebar'

export interface ServiceMainPageProps {
  children: React.ReactNode
  sideBarSettings: {
    additionalProjectLinks?: SideBarLink[]
    globalLinks?: SideBarLink[]
  }
}

export function ServiceMainPage({
  children,
  sideBarSettings: { additionalProjectLinks = [], globalLinks = [] }
}: ServiceMainPageProps) {
  const { projectId } = useParams()
  const getSideBarSize = () => (projectId || globalLinks.length > 0 ? 65 : 0)

  const [sideBarSize, setSideBarSize] = useState(() => getSideBarSize())

  useEffect(() => {
    setSideBarSize(getSideBarSize())
  }, [projectId, globalLinks.length > 0])

  return (
    <Box
      display={'grid'}
      gridTemplateColumns={`${sideBarSize}px 1px calc(100% - ${sideBarSize}px - 1px)`}
      alignItems={'start'}
      sx={{ transition: '225ms ease-in-out' }}
    >
      <Box sx={{ position: 'sticky', top: 0, left: 0, overflow: 'hidden' }}>
        <SideBar
          projectId={projectId}
          additionalProjectLinks={additionalProjectLinks}
          globalLinks={globalLinks}
        />
      </Box>
      <Divider orientation="vertical" />
      <Box>{children}</Box>
    </Box>
  )
}
