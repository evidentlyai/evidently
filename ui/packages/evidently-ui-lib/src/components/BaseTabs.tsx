import React, { ReactNode } from 'react'

import { Box, Tab, Tabs } from '@mui/material'

export interface TabInfo {
  title: string
  tab: ReactNode
  link?: string
  disabled?: boolean
  icon?: ReactNode
}

interface BaseTabsProps {
  activeTab: number
  tabs: TabInfo[]
  tabStyle?: string
  onNewTabSelected: (event: React.SyntheticEvent, newTabIdx: number) => void
}

const BaseTabs: React.FunctionComponent<BaseTabsProps> = (props) => {
  const activeTab = props.activeTab === -1 ? 0 : props.activeTab
  return (
    <div>
      <Tabs
        value={activeTab}
        onChange={props.onNewTabSelected}
        indicatorColor="primary"
        textColor="primary"
      >
        {props.tabs.map((ti, idx) => (
          <Tab
            // className={idx === activeTab ? props.classes.activeTab : props.classes.tab}
            disabled={ti.disabled ?? false}
            key={idx}
            label={
              <Box className={props.tabStyle}>
                <Box display={'flex'} sx={{ fontSize: '0.875rem' }}>
                  <span>{ti.icon}</span>
                  {ti.title}
                </Box>
              </Box>
            }
          />
        ))}
      </Tabs>
      <Box>
        {props.tabs.map((ti, idx) => (
          <div key={idx} hidden={(props.activeTab === -1 ? 0 : props.activeTab) !== idx}>
            {(props.activeTab === -1 ? 0 : props.activeTab) !== idx ? <div /> : ti.tab}
          </div>
        ))}
      </Box>
    </div>
  )
}

export default BaseTabs
