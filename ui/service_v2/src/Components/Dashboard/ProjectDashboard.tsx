import { EditTabButton } from 'Components/Dashboard/EditTabsButton'
import { AnchorLogo } from 'Components/custom-icons/anchor'
import type { DashboardModel } from 'api/types'
import { useProjectInfo } from 'contexts/project'
import { widgetWrapperContext } from 'evidently-ui-lib/contexts/WidgetWrapper'
import { useToggle } from 'evidently-ui-lib/hooks/index'
import { Edit as EditIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { Delete as DeleteIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { Addchart as AddchartIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import {
  Box,
  IconButton,
  Link as MuiLink,
  Stack,
  Tab,
  Tabs,
  ToggleButton,
  Tooltip
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useIsAnyLoaderOrActionRunning } from 'hooks'
import { RouterLink } from 'new-routes/components'
import { useSubmitFetcher } from 'new-routes/hooks'
import { useMemo, useState } from 'react'
import React from 'react'
import invariant from 'tiny-invariant'
import { AddNewTabButton } from './AddNewTabButton'
import { DrawDashboardPanels } from './DrawDashboardPanels'

const GlobalDataForPanelWrapper = React.createContext<{
  editMode: boolean
  allPanels: DashboardModel['panels']
}>({ editMode: false, allPanels: [] })

const useGlobalDataForPanelWrapper = () => React.useContext(GlobalDataForPanelWrapper)

type TabStrict = {
  id: string
  title: string
  panels: string[]
}

export const DashboardPanelsWithTabs = ({
  data: { panels: allPanels, tabs: allTabs }
}: { data: DashboardModel }) => {
  const { project } = useProjectInfo()
  invariant(project, 'missing project')

  const { id: projectId } = project

  const [editMode, toggleEditMode] = useToggle(false)

  // TODO: Please fix this `DashboardTab` type to be strict on backend
  const tabs = useMemo(
    () => allTabs.filter((e): e is TabStrict => Boolean(e.id && e.title)),
    [allTabs]
  )

  const panelsForTabs = useMemo(
    () =>
      tabs.map(({ panels: panel_ids }) =>
        allPanels.filter((panel) => panel.id && panel_ids.includes(panel.id))
      ),
    [tabs, allPanels]
  )

  const isLoading = useIsAnyLoaderOrActionRunning()

  const allTabsMeppedPanelIds = panelsForTabs.flat().map(({ id }) => id)
  const restPanels = allPanels.filter(({ id }) => !allTabsMeppedPanelIds.includes(id))
  const isShowRestTab = restPanels.length > 0

  const getTabIdByPanelId = (panelId: string) => {
    const index = panelsForTabs.findIndex((panels) => panels.some(({ id }) => id === panelId))
    return index >= 0 ? index : restPanels.some(({ id }) => id === panelId) ? tabs.length : 0
  }

  const [tabIndex, setTabIndex] = useState(() => {
    if (!window.location.hash) {
      return 0
    }

    const panelId = window.location.hash.slice(1)
    return getTabIdByPanelId(panelId)
  })

  if (tabIndex !== 0 && tabIndex > tabs.length + (isShowRestTab ? 0 : -1)) {
    setTabIndex(0)
  }

  const createNewTabFetcher = useSubmitFetcher({
    path: '/v2/projects/:projectId/dashboard',
    action: 'create-tab'
  })

  const renameTabFetcher = useSubmitFetcher({
    path: '/v2/projects/:projectId/dashboard',
    action: 'rename-tab'
  })

  const deleteTabsFetcher = useSubmitFetcher({
    path: '/v2/projects/:projectId/dashboard',
    action: 'delete-tabs'
  })

  const EditTabsControlsRendered = (
    <>
      <AddNewTabButton />
      <EditTabButton
        tabs={tabs}
        initialTabIndex={tabIndex}
        onDeleteTabs={(data) => deleteTabsFetcher.submit({ data, paramsToReplace: { projectId } })}
        onRenameTab={(data) => renameTabFetcher.submit({ data, paramsToReplace: { projectId } })}
        createTab={{
          version: 'v2',
          onCreateTab: (data) =>
            createNewTabFetcher.submit({ data, paramsToReplace: { projectId } })
        }}
      />
    </>
  )

  const AddPanelButtonRendered = (
    <Tooltip title='Add Panel'>
      <Box>
        <RouterLink
          type='icon'
          to={'/v2/projects/:projectId/dashboard/panel'}
          paramsToReplace={{ projectId }}
          IconButtonProps={{ disabled: isLoading, children: <AddchartIcon /> }}
        />
      </Box>
    </Tooltip>
  )

  const globalData = { tabs, tabIndex, allPanels, editMode }

  if (tabs.length === 0) {
    // have no tabs
    return (
      <>
        <Box
          py={2}
          display={'flex'}
          alignItems={'center'}
          justifyContent={'flex-end'}
          columnGap={2}
        >
          <>
            {editMode && (
              <Stack direction={'row'} flex={1} gap={1}>
                {EditTabsControlsRendered}
              </Stack>
            )}
            {editMode && AddPanelButtonRendered}
            <Tooltip title='Edit Mode'>
              <ToggleButton
                value={'check'}
                selected={editMode}
                sx={{ border: 'none', borderRadius: '50%' }}
                onChange={() => toggleEditMode()}
              >
                <EditIcon />
              </ToggleButton>
            </Tooltip>
          </>
        </Box>

        <GlobalDataForPanelWrapper.Provider value={globalData}>
          <widgetWrapperContext.Provider value={{ WidgetWrapper: PanelWrapper }}>
            <DrawDashboardPanels panels={allPanels} />
          </widgetWrapperContext.Provider>
        </GlobalDataForPanelWrapper.Provider>
      </>
    )
  }

  return (
    <>
      <Box pl={1} pr={4} display={'flex'} gap={2} justifyContent={'space-between'}>
        <Tabs
          sx={{ maxWidth: { xs: 1, md: 0.85 } }}
          value={tabIndex}
          onChange={(_, value) => setTabIndex(value)}
          variant='scrollable'
          scrollButtons='auto'
          selectionFollowsFocus
          allowScrollButtonsMobile
        >
          {tabs.map(({ id, title }) => (
            <Tab key={id} label={title} />
          ))}

          {isShowRestTab && <Tab label={'(Others)'} />}
        </Tabs>

        <Box display={'flex'} justifyContent={'space-between'} alignItems={'center'} flexGrow={1}>
          <Box display={'flex'} columnGap={1}>
            {editMode && EditTabsControlsRendered}
          </Box>

          <Box display={'flex'} alignItems={'center'} columnGap={2}>
            {editMode && AddPanelButtonRendered}
            <Tooltip title='Edit Mode'>
              <ToggleButton
                value={'check'}
                selected={editMode}
                size='small'
                sx={{ border: 'none', borderRadius: '50%' }}
                onChange={() => toggleEditMode()}
              >
                <EditIcon />
              </ToggleButton>
            </Tooltip>
          </Box>
        </Box>
      </Box>

      <Box p={2}>
        <GlobalDataForPanelWrapper.Provider value={globalData}>
          <widgetWrapperContext.Provider value={{ WidgetWrapper: PanelWrapper }}>
            {panelsForTabs.map((tabPanels, index) => (
              <Box key={tabs[index].id}>
                {index === tabIndex && <DrawDashboardPanels panels={tabPanels} />}
              </Box>
            ))}

            <Box>
              {isShowRestTab && tabIndex === tabs.length && (
                <DrawDashboardPanels panels={restPanels} />
              )}
            </Box>
          </widgetWrapperContext.Provider>
        </GlobalDataForPanelWrapper.Provider>
      </Box>
    </>
  )
}

const PanelWrapper = ({ id: panelId, children }: { id: string; children: React.ReactNode }) => {
  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project

  const { editMode } = useGlobalDataForPanelWrapper()

  const deletePanelsFetcher = useSubmitFetcher({
    path: '/v2/projects/:projectId/dashboard',
    action: 'delete-panels'
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <Box id={panelId}>
      {editMode && (
        <Box position={'relative'}>
          <Box
            sx={{
              zIndex: 1,
              backdropFilter: 'blur(5px)',
              bgcolor: '#ffd5d542',
              borderRadius: '20px',
              p: 1,
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              position: 'absolute',
              top: '7px',
              right: '10px'
            }}
          >
            <Tooltip
              title='Copy link'
              onClick={() => {
                setTimeout(() => navigator.clipboard.writeText(window.location.href), 10)
              }}
            >
              <MuiLink href={`#${panelId}`}>
                <IconButton disabled={isLoading}>
                  <AnchorLogo />
                </IconButton>
              </MuiLink>
            </Tooltip>

            <Tooltip title='Edit Panel'>
              <Box>
                <RouterLink
                  type='icon'
                  to={'/v2/projects/:projectId/dashboard/panel'}
                  query={{ edit_panel_id: panelId }}
                  paramsToReplace={{ projectId }}
                  IconButtonProps={{ disabled: isLoading, children: <EditIcon /> }}
                />
              </Box>
            </Tooltip>

            <Tooltip title='Delete panel'>
              <IconButton
                aria-label='delete'
                onClick={() => {
                  if (confirm('Are you sure you want to delete this panel?') === true) {
                    deletePanelsFetcher.submit({ data: [panelId], paramsToReplace: { projectId } })
                  }
                }}
                disabled={isLoading}
              >
                <DeleteIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      )}

      <Box>{children}</Box>
    </Box>
  )
}
