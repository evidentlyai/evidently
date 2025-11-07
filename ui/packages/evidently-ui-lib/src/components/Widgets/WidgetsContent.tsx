import { Box, Grid, Stack, Tab, Tabs } from '@mui/material'
import React from 'react'
import { useState } from 'react'
import type { WidgetInfo } from '~/api'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

export const AdditionalComponents = React.createContext<{
  Component?: ({ variant }: { variant: VARIANTS }) => JSX.Element
}>({})

const useAdditionalComponents = () => React.useContext(AdditionalComponents)

export const DrawWidgets: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => (
  <Grid container spacing={3} direction='row' alignItems='stretch'>
    {widgets.map((widgetInfo) => (
      <WidgetRenderer key={widgetInfo.id} info={widgetInfo} />
    ))}
  </Grid>
)

export const SnapshotWidgets: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => (
  <SnapshotWidgetsDispatcher widgets={widgets} />
)

const SnapshotWidgetsDispatcher: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => {
  const v2TestWidgets = widgets.filter(testIsV2TestPredicate)

  if (v2TestWidgets.length > 0) {
    return <SnapshotWidgetsV2 widgets={widgets} />
  }

  return <SnapshotWidgetsV1 widgets={widgets} />
}

export type VARIANTS = 'metrics' | 'tests'

const SnapshotWidgetsV1: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => {
  const { Component } = useAdditionalComponents()

  const isTestSuite = widgets.some(isTestSuitePredicate)

  return (
    <>
      {Component && <Component variant={isTestSuite ? 'tests' : 'metrics'} />}

      <DrawWidgets widgets={widgets} />
    </>
  )
}

const SnapshotWidgetsV2: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => {
  const [v2Tab, setV2Tab] = useState<VARIANTS>('metrics')

  const metrics = widgets.filter((w) => !testIsV2TestPredicate(w))
  const tests = widgets.filter((w) => testIsV2TestPredicate(w))

  const { Component } = useAdditionalComponents()

  return (
    <Box>
      <Stack direction={'row'} alignItems={'center'} justifyContent={'flex-end'}>
        <Tabs
          value={v2Tab}
          onChange={(_, v2Tab) => setV2Tab(v2Tab as VARIANTS)}
          textColor='secondary'
          indicatorColor='secondary'
          aria-label='secondary tabs example'
        >
          <Tab value={'metrics' satisfies VARIANTS} label='Metrics' />
          <Tab value={'tests' satisfies VARIANTS} label='Tests' />
        </Tabs>
      </Stack>

      {Component && <Component variant={v2Tab} />}

      {v2Tab === 'metrics' && <DrawWidgets widgets={metrics} />}
      {v2Tab === 'tests' && <DrawWidgets widgets={tests} />}
    </Box>
  )
}

const testIsV2TestPredicate = (w: WidgetInfo) => w.params && 'v2_test' in w.params
const isTestSuitePredicate = (w: WidgetInfo) => w.type === 'test_suite'
