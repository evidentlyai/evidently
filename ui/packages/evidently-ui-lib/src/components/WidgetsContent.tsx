import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined'
import { Box, Chip, Grid, IconButton, Stack, Tab, Tabs, Tooltip } from '@mui/material'
import { useState } from 'react'
import type { WidgetInfo } from '~/api'
import { WidgetRenderer } from '~/widgets/WidgetRenderer'

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

type V2_TABS = 'metrics' | 'tests'

const SnapshotWidgetsV2: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => {
  const [v2Tab, setV2Tab] = useState<V2_TABS>('metrics')

  const metrics = widgets.filter((w) => !testIsV2TestPredicate(w))
  const tests = widgets.filter((w) => testIsV2TestPredicate(w))

  return (
    <Box>
      <Stack direction={'row'} alignItems={'center'} justifyContent={'space-between'}>
        <Stack direction={'row'} alignItems={'center'} gap={0.5}>
          <Chip label={'New version ✨'} variant='outlined' color='primary' />

          <Tooltip
            arrow
            placement='top'
            title='This report contains both mertics and tests. You can switch between them'
          >
            <IconButton size='small'>
              <InfoOutlinedIcon fontSize='inherit' />
            </IconButton>
          </Tooltip>
        </Stack>

        <Tabs
          value={v2Tab}
          onChange={(_, v2Tab) => setV2Tab(v2Tab as V2_TABS)}
          textColor='secondary'
          indicatorColor='secondary'
          aria-label='secondary tabs example'
        >
          <Tab value={'metrics' satisfies V2_TABS} label='Metrics' />
          <Tab value={'tests' satisfies V2_TABS} label='Tests' />
        </Tabs>
      </Stack>

      {v2Tab === 'metrics' && <SnapshotWidgetsV1 widgets={metrics} />}
      {v2Tab === 'tests' && <SnapshotWidgetsV1 widgets={tests} />}
    </Box>
  )
}

const SnapshotWidgetsV1: React.FC<{ widgets: WidgetInfo[] }> = ({ widgets }) => (
  <DrawWidgets widgets={widgets} />
)

const testIsV2TestPredicate = (w: WidgetInfo) => w.params && 'v2_test' in w.params
