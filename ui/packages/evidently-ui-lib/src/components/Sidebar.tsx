import { Link as RouterLink } from 'react-router-dom'
import { IconButton, Link, Stack, Tooltip } from '@mui/material'

import DashboardOutlinedIcon from '@mui/icons-material/Dashboard'
import ChecklistOutlinedIcon from '@mui/icons-material/Checklist'
import SummarizeOutlinedIcon from '@mui/icons-material/Summarize'

export const ICONS_FONS_SIZE = 30

const BaseLinks = [
  {
    label: 'Dashboard',
    icon: <DashboardOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: ''
  },
  {
    label: 'Reports',
    icon: <SummarizeOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: 'reports'
  },
  {
    label: 'Test Suites',
    icon: <ChecklistOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: 'test-suites'
  }
] as const

export const ProjectSideBar = ({
  projectId,
  additionalLinks = []
}: {
  projectId?: string
  additionalLinks?: { label: string; icon: React.ReactNode; path: string }[]
}) => {
  return (
    <nav aria-label="project navigation">
      <Stack direction={'column'} alignItems={'center'} useFlexGap gap={1}>
        {[...BaseLinks, ...additionalLinks].map((link) => (
          <Tooltip key={link.path} placement="right" title={link.label}>
            <Link
              component={RouterLink}
              relative="route"
              to={['projects', projectId, link.path].filter(Boolean).join('/')}
            >
              <IconButton size="large">{link.icon}</IconButton>
            </Link>
          </Tooltip>
        ))}
      </Stack>
    </nav>
  )
}
