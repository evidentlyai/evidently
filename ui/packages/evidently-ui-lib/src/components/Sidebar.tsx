import { Link as RouterLink, useMatches } from 'react-router-dom'
import { Divider, IconButton, Link, Stack, Tooltip } from '@mui/material'

import DashboardOutlinedIcon from '@mui/icons-material/Dashboard'
import ChecklistOutlinedIcon from '@mui/icons-material/Checklist'
import SummarizeOutlinedIcon from '@mui/icons-material/Summarize'

export const ICONS_FONS_SIZE = 25

export type SideBarLink = {
  id: string
  label: string
  icon: React.ReactNode
  path: string
}

const BaseProjectLinks = [
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
] satisfies SideBarLink[]

export const SideBar = ({
  projectId,
  globalLinks: globalLevelLinks = [],
  additionalProjectLinks = []
}: {
  projectId?: string
  globalLinks?: SideBarLink[]
  additionalProjectLinks?: SideBarLink[]
}) => {
  const matches = useMatches()
  const projectLinks = [...BaseProjectLinks, ...additionalProjectLinks]
  const activeIndex = projectLinks.findIndex(({ id }) => matches.map(({ id }) => id).includes(id))
  return (
    <nav aria-label="project navigation">
      <Stack direction={'column'} alignItems={'center'} useFlexGap gap={1}>
        {globalLevelLinks.length > 0 && (
          <>
            {globalLevelLinks.map((link, index) => (
              <Tooltip key={link.path} placement="right" title={link.label}>
                <Link component={RouterLink} to={'/' + link.path}>
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
            <Divider flexItem orientation="horizontal" />
          </>
        )}
        {projectLinks.map((link, index) => (
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
