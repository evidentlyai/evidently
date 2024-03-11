import React, { ReactNode } from 'react'

import { Grid, Card, CardContent, Typography } from '@mui/material'

import { WidgetInfo } from '~/api'

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

const Widget2 = (props: WidgetProps) => {
  const { size } = props
  const alertsPosition = props.children.alertsPosition ?? 'row'
  const { title, details, content, alerts, insights } = props.children
  const isAlertsExists = alerts === undefined ? false : alerts.length > 0
  const isInsightsExists = insights === undefined ? false : insights.length > 0
  // const classes = useStyles();
  return (
    <Grid
      item
      {...Sizes(size)}
      // className={classes.widget}
    >
      <Card
        sx={{
          border: '1px solid',
          borderColor: '#d7cccc',
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
                    // className={classes.alertArea}
                  ></Grid>
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
              </React.Fragment>
            )}
            {isInsightsExists ? insights!.map(() => <Grid item xs sm md></Grid>) : <div />}
          </Grid>
        </CardContent>
      </Card>
    </Grid>
  )
}

export default Widget2
