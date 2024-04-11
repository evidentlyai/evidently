import { Link as RouterLink, useMatches } from 'react-router-dom'
import { IconButton, Link, Stack, Tooltip } from '@mui/material'

import DashboardOutlinedIcon from '@mui/icons-material/Dashboard'
import ChecklistOutlinedIcon from '@mui/icons-material/Checklist'
import SummarizeOutlinedIcon from '@mui/icons-material/Summarize'

export const ICONS_FONS_SIZE = 30

export type SideBarLink = { id: string; label: string; icon: React.ReactNode; path: string }

const BaseLinks = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: <DashboardOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: ''
  },
  {
    id: 'reports',
    label: 'Reports',
    icon: <SummarizeOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: 'reports'
  },
  {
    id: 'test_suites',
    label: 'Test Suites',
    icon: <ChecklistOutlinedIcon sx={{ fontSize: ICONS_FONS_SIZE }} />,
    path: 'test-suites'
  }
] as const

export const SideBar = ({
  projectId,
  additionalLinks = []
}: {
  projectId?: string
  additionalLinks?: SideBarLink[]
}) => {
  const matches = useMatches()
  const links = [...BaseLinks, ...additionalLinks]
  const activeIndex = links.findIndex(({ id }) => matches.map(({ id }) => id).includes(id))
  return (
    <nav aria-label="project navigation">
      <Stack direction={'column'} alignItems={'center'} useFlexGap gap={1}>
        {links.map((link, index) => (
          <Tooltip key={link.path} placement="right" title={link.label}>
            <Link
              component={RouterLink}
              to={['projects', projectId, link.path].filter(Boolean).join('/')}
            >
              <IconButton
                sx={[
                  { borderRadius: 3 },
                  activeIndex === index && {
                    color: (theme) => theme.palette.secondary.main,
                    backgroundColor: (theme) => theme.palette.primary.light
                  }
                ]}
                size="large"
              >
                {link.icon}
              </IconButton>
            </Link>
          </Tooltip>
        ))}
      </Stack>
    </nav>
  )
}
