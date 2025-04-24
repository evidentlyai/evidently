import type { DashboardModel } from 'evidently-ui-lib/api/types'
import { widgetWrapperContext } from 'evidently-ui-lib/contexts/WidgetWrapper'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useMemo, useState } from 'react'
import React from 'react'
import { DrawDashboardPanels } from './DrawDashboardPanels'

const GlobalDataForPanelWrapper = React.createContext<{
  allPanels: DashboardModel['panels']
}>({ allPanels: [] })

type TabStrict = {
  id: string
  title: string
  panels: string[]
}

export const DashboardPanelsWithTabs = ({
  data: { panels: allPanels, tabs: allTabs }
}: { data: DashboardModel }) => {
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

  const globalData = { tabs, tabIndex, allPanels }

  if (tabs.length === 0) {
    // have no tabs
    return (
      <>
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
      <Box p={2}>
        <GlobalDataForPanelWrapper.Provider value={globalData}>
          <widgetWrapperContext.Provider value={{ WidgetWrapper: PanelWrapper }}>
            <Box>
              <DrawDashboardPanels panels={allPanels} />
            </Box>
          </widgetWrapperContext.Provider>
        </GlobalDataForPanelWrapper.Provider>
      </Box>
    </>
  )
}

const PanelWrapper = ({ id: panelId, children }: { id: string; children: React.ReactNode }) => {
  return (
    <Box id={panelId}>
      <Box>{children}</Box>
    </Box>
  )
}
