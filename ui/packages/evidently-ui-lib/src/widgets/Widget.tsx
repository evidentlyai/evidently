import React, { type ReactNode } from 'react'
import type { WidgetInfo } from '~/api'

import { Card, CardContent, Grid, Typography } from '@mui/material'

import { useWidgetWrapper } from '~/contexts/WidgetWrapper'
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

const Widget = (props: WidgetProps) => {
  const { size } = props
  const alertsPosition = props.children.alertsPosition ?? 'row'
  const { id, title, details, content, alerts, alertStats, insights } = props.children
  const isAlertsExists = alerts === undefined ? false : alerts.length > 0
  const isInsightsExists = insights === undefined ? false : insights.length > 0

  const { WidgetWrapper } = useWidgetWrapper()

  return (
    <Grid size={Sizes(size)}>
      <WidgetWrapper id={id}>
        <Card elevation={0}>
          <CardContent>
            <Grid container spacing={1} direction={'column'}>
              {alertsPosition === 'row' ? (
                <Grid container spacing={1}>
                  <Grid size={isAlertsExists && alertsPosition === 'row' ? 9 : 12}>
                    {title ? (
                      <Typography fontWeight={500} variant={'h5'}>
                        {title}
                      </Typography>
                    ) : (
                      <></>
                    )}
                    <div>{content}</div>
                    {details ? <Typography variant={'subtitle1'}>{details}</Typography> : <></>}
                  </Grid>
                  {isAlertsExists ? (
                    <Grid
                      container
                      spacing={1}
                      direction={'column'}
                      justifyContent={'center'}
                      size={3}
                    >
                      {alerts ? (
                        <React.Fragment>
                          {alertStats ? (
                            <Grid>
                              <AlertStatBlock
                                alertStats={alertStats}
                                // classes={classes}
                              />
                            </Grid>
                          ) : (
                            <></>
                          )}
                          {alerts.map((alert) => (
                            // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                            <Grid>
                              <AlertBlock data={alert} />
                            </Grid>
                          ))}
                        </React.Fragment>
                      ) : (
                        <></>
                      )}
                    </Grid>
                  ) : (
                    <></>
                  )}
                </Grid>
              ) : (
                <React.Fragment>
                  <Grid>
                    {title ? <Typography variant={'h5'}>{title}</Typography> : <></>}
                    <div>{content}</div>
                    {details ? <Typography variant={'subtitle1'}>{details}</Typography> : <></>}
                  </Grid>
                  {isAlertsExists ? (
                    <Grid size={'grow'}>
                      <Grid container direction={'row'} spacing={1}>
                        {alerts ? (
                          <React.Fragment>
                            {alertStats ? (
                              <Grid size={'grow'}>
                                <AlertStatBlock
                                  alertStats={alertStats}
                                  // classes={classes}
                                />
                              </Grid>
                            ) : (
                              <></>
                            )}
                            {alerts.map((alert) => (
                              // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                              <Grid size={'grow'}>
                                <AlertBlock data={alert} />
                              </Grid>
                            ))}
                          </React.Fragment>
                        ) : (
                          <></>
                        )}
                      </Grid>
                    </Grid>
                  ) : (
                    <></>
                  )}
                </React.Fragment>
              )}
              {isInsightsExists ? (
                insights?.map((insight) => (
                  // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                  <Grid size={'grow'}>
                    <InsightBlock data={insight} />
                  </Grid>
                ))
              ) : (
                <></>
              )}
            </Grid>
          </CardContent>
        </Card>
      </WidgetWrapper>
    </Grid>
  )
}

export default Widget
