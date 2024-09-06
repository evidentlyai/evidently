import React, { type ReactNode } from 'react'
import type { WidgetInfo } from '~/api'

import { Card, CardContent, Grid, Typography } from '@mui/material'

import AlertBlock from './AlertBlock'
import AlertStatBlock from './AlertStatBlock'
import InsightBlock from './InsightBlock'

/***
 * base part of widget to control:
 *  - layouts
 *  - colors
 */

export interface WidgetProps {
  size: 1 | 3 | 6 | 12
  alertPosition?: 'row' | 'column'
  children: WidgetInfo & { content: ReactNode }
}

interface sizes {
  xs: 1 | 3 | 6 | 12
  sm: 1 | 3 | 6 | 12
  md: 1 | 3 | 6 | 12
  lg: 1 | 3 | 6 | 12
}

function Sizes(size: number): sizes {
  if (size === 12) {
    return {
      xs: 12,
      sm: 12,
      md: 12,
      lg: 12
    }
  }
  if (size === 6) {
    return {
      xs: 12,
      sm: 12,
      md: 6,
      lg: 6
    }
  }
  if (size === 3) {
    return {
      xs: 12,
      sm: 6,
      md: 3,
      lg: 3
    }
  }
  return {
    xs: 6,
    sm: 3,
    md: 1,
    lg: 1
  }
}

const Widget = (
  props: WidgetProps & {
    ItemWrapper?: ({ id, children }: { id: string; children: React.ReactNode }) => React.ReactNode
  }
) => {
  const { size, ItemWrapper } = props
  const alertsPosition = props.children.alertsPosition ?? 'row'
  const { id, title, details, content, alerts, alertStats, insights } = props.children
  const isAlertsExists = alerts === undefined ? false : alerts.length > 0
  const isInsightsExists = insights === undefined ? false : insights.length > 0
  const Component = (
    <Card
      sx={{
        border: '1px solid',
        borderColor: '#d6d6d6',
        borderRadius: '4px'
      }}
      elevation={0}
    >
      <CardContent>
        <Grid container spacing={1} direction={'column'}>
          {alertsPosition === 'row' ? (
            <Grid container spacing={1} item>
              <Grid item xs={isAlertsExists && alertsPosition === 'row' ? 9 : 12}>
                {title ? (
                  <Typography fontWeight={500} variant={'h5'}>
                    {title}
                  </Typography>
                ) : (
                  <div />
                )}
                <div>{content}</div>
                {details ? <Typography variant={'subtitle1'}>{details}</Typography> : <div />}
              </Grid>
              {isAlertsExists ? (
                <Grid
                  container
                  spacing={1}
                  direction={'column'}
                  justifyContent={'center'}
                  item
                  xs={3}
                >
                  {alerts ? (
                    <React.Fragment>
                      {alertStats ? (
                        <Grid item>
                          <AlertStatBlock
                            alertStats={alertStats}
                            // classes={classes}
                          />
                        </Grid>
                      ) : (
                        <div />
                      )}
                      {alerts.map((alert) => (
                        // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                        <Grid item>
                          <AlertBlock data={alert} />
                        </Grid>
                      ))}
                    </React.Fragment>
                  ) : (
                    <div />
                  )}
                </Grid>
              ) : (
                <div />
              )}
            </Grid>
          ) : (
            <React.Fragment>
              <Grid item>
                {title ? <Typography variant={'h5'}>{title}</Typography> : <div />}
                <div>{content}</div>
                {details ? <Typography variant={'subtitle1'}>{details}</Typography> : <div />}
              </Grid>
              {isAlertsExists ? (
                <Grid item xs>
                  <Grid container direction={'row'} spacing={1}>
                    {alerts ? (
                      <React.Fragment>
                        {alertStats ? (
                          <Grid item xs>
                            <AlertStatBlock
                              alertStats={alertStats}
                              // classes={classes}
                            />
                          </Grid>
                        ) : (
                          <div />
                        )}
                        {alerts.map((alert) => (
                          // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                          <Grid item xs>
                            <AlertBlock data={alert} />
                          </Grid>
                        ))}
                      </React.Fragment>
                    ) : (
                      <div />
                    )}
                  </Grid>
                </Grid>
              ) : (
                <div />
              )}
            </React.Fragment>
          )}
          {isInsightsExists ? (
            insights?.map((insight) => (
              // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
              <Grid item xs sm md>
                <InsightBlock data={insight} />
              </Grid>
            ))
          ) : (
            <div />
          )}
        </Grid>
      </CardContent>
    </Card>
  )

  return (
    <Grid item {...Sizes(size)}>
      {ItemWrapper ? ItemWrapper({ id, children: Component }) : Component}
    </Grid>
  )
}

export default Widget
