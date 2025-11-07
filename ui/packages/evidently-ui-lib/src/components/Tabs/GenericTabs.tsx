import { Tab, Tabs } from 'evidently-ui-lib/shared-dependencies/mui-material'

type TabType = { label: string; key: string }

export type GenericTabsProps<Tabs extends TabType> = {
  activeTab: Tabs['key']
  onTabChange: (newTab: Tabs['key']) => void
  tabs: Tabs[]
  size?: keyof typeof sizeTokens
}

export const GenericTabs = <Tabs extends TabType>(props: GenericTabsProps<Tabs>) => {
  const { activeTab, onTabChange, tabs, size = 'medium' } = props

  const tokens = sizeTokens[size]
  return (
    <Tabs
      sx={(t) => ({
        '& .MuiTabs-indicator': { display: 'none' },
        '& .MuiTabs-flexContainer': {
          gap: tokens.containerGap,
          width: 'fit-content',
          borderRadius: 2,
          backgroundColor: 'grey.900',
          ...t.applyStyles('light', { backgroundColor: '#f5f5f5' }),
          p: tokens.containerPadding
        }
      })}
      value={activeTab}
      onChange={(_, newValue) => onTabChange(newValue)}
    >
      {tabs.map((tab) => (
        <Tab
          sx={(t) => ({
            minHeight: 'unset',
            borderRadius: 1.5,
            textTransform: 'none',
            fontWeight: 500,
            fontSize: tokens.tabFontSize,
            color: 'text.secondary',
            transition: t.transitions.create(['background-color', 'color'], {
              duration: t.transitions.duration.short
            }),
            padding: tokens.tabPadding,
            '&.Mui-selected': { color: 'text.primary', backgroundColor: 'divider' },
            '&:hover': { backgroundColor: 'action.selected' }
          })}
          key={tab.key}
          label={tab.label}
          value={tab.key}
        />
      ))}
    </Tabs>
  )
}

const sizeTokens = {
  medium: { containerGap: 1, containerPadding: 0.75, tabPadding: 1, tabFontSize: '0.875rem' },
  large: { containerGap: 1.25, containerPadding: 0.875, tabPadding: 1, tabFontSize: '1rem' }
} as const
