import { Button, Grid } from '@mui/material'
import React from 'react'
import type { WidgetListParams } from '~/api'
import WidgetPanel from './WidgetPanel'
import { WidgetRenderer } from './WidgetRenderer'

import ArrowLeftIcon from '@mui/icons-material/ArrowLeft'
import ArrowRightIcon from '@mui/icons-material/ArrowRight'

const WidgetList: React.FunctionComponent<WidgetListParams & { widgetSize: number }> = (params) => {
  const [pageState, setPageState] = React.useState({ page: 0 })
  const drawWidgets = params.widgets.slice(
    pageState.page * params.pageSize,
    (pageState.page + 1) * params.pageSize
  )
  return (
    <WidgetPanel>
      {drawWidgets.map((wi, idx) => WidgetRenderer(`wi_${idx}`, wi))}
      <Grid item xs={12}>
        <Button
          startIcon={<ArrowLeftIcon />}
          disabled={pageState.page === 0}
          onClick={() => setPageState((prev) => ({ page: prev.page - 1 }))}
        >
          Previous
        </Button>
        <span>
          {pageState.page + 1} / {Math.round(params.widgets.length / params.pageSize)}
        </span>
        <Button
          endIcon={<ArrowRightIcon />}
          disabled={pageState.page >= params.widgets.length / params.pageSize - 1}
          onClick={() => setPageState((prev) => ({ page: prev.page + 1 }))}
        >
          Next
        </Button>
      </Grid>
    </WidgetPanel>
  )
}

export default WidgetList
