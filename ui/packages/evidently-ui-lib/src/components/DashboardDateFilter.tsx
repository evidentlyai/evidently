import {
  AlertTitle,
  Box,
  Collapse,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Switch,
  Typography
} from '@mui/material'

import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'

import dayjs, { type Dayjs } from 'dayjs'
import 'dayjs/locale/en-gb'
import 'dayjs/plugin/duration'

import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import { AlertThemed } from '~/components/AlertThemed'

export type ShowInOrderSwitchProps = {
  isXaxisAsCategorical: boolean
  setIsXaxisAsCategorical: React.Dispatch<React.SetStateAction<boolean>>
}

export const ShowInOrderSwitch = ({
  setIsXaxisAsCategorical,
  isXaxisAsCategorical
}: ShowInOrderSwitchProps) => {
  return (
    <Box minWidth={180} display={'flex'} justifyContent={'center'}>
      <FormControlLabel
        control={
          <Switch
            checked={isXaxisAsCategorical}
            onChange={(event) => setIsXaxisAsCategorical(event.target.checked)}
          />
        }
        label='Show in order'
      />
    </Box>
  )
}

export type DateFilterState = {
  dateFrom?: Dayjs | null
  dateTo?: Dayjs | null
}

export interface DateFilterProps {
  dates: DateFilterState
  setDates: React.Dispatch<React.SetStateAction<DateFilterState>>
  required?: boolean
  children?: React.ReactNode
}

export const DateFilter = ({ dates, setDates, children, required = false }: DateFilterProps) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <Grid
        container
        padding={1}
        zIndex={1}
        gap={2}
        justifyContent='flex-start'
        alignItems={'flex-end'}
      >
        <>
          {children && <Grid item>{children}</Grid>}
          <Grid item xs={12} md={2}>
            <FormControl fullWidth>
              <InputLabel>Period</InputLabel>
              <Select
                variant='standard'
                defaultValue={''}
                onChange={(event) => {
                  const [valueStr, durationStr] = (event.target.value as string).split(',')

                  if (valueStr === '') {
                    setDates({ dateFrom: null, dateTo: null })
                    return
                  }

                  const now = dayjs()
                  const [value, duration] = [Number(valueStr), durationStr]
                  const lastDate = now.subtract(value, duration as dayjs.ManipulateType)

                  setDates({ dateFrom: lastDate, dateTo: now })
                }}
              >
                <MenuItem value={''}>
                  <em>None</em>
                </MenuItem>
                <MenuItem value={'10,minutes'}>Last 10 Minutes</MenuItem>
                <MenuItem value={'30,minutes'}>Last 30 Minutes</MenuItem>
                <MenuItem value={'1,hours'}>Last 1 Hours</MenuItem>
                <MenuItem value={'2,hours'}>Last 2 Hours</MenuItem>
                <MenuItem value={'8,hours'}>Last 8 Hours</MenuItem>
                <MenuItem value={'24,hours'}>Last 24 Hours</MenuItem>
                <MenuItem value={'7,days'}>Last 7 Days</MenuItem>
                <MenuItem value={'14,days'}>Last 14 Days</MenuItem>
                <MenuItem value={'28,days'}>Last 28 Days</MenuItem>
                <MenuItem value={'60,days'}>Last 60 Days</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item>
            <Box display={'flex'} alignItems={'center'} gap={2}>
              <DateTimePicker
                minDate={undefined}
                maxDate={dates?.dateTo}
                slotProps={{
                  textField: {
                    variant: 'standard',
                    error: required ? !dates.dateFrom : undefined
                  }
                }}
                label='From'
                value={dates?.dateFrom}
                onChange={(value) => setDates((prev) => ({ ...prev, dateFrom: value }))}
              />
              <Box height={1} display={'flex'} alignItems={'center'}>
                <Typography> - </Typography>
              </Box>
              <DateTimePicker
                minDate={dates?.dateFrom}
                maxDate={undefined}
                slotProps={{
                  textField: {
                    variant: 'standard',
                    error: required ? !dates.dateTo : undefined
                  }
                }}
                label='To'
                value={dates?.dateTo}
                onChange={(value) => setDates((prev) => ({ ...prev, dateTo: value }))}
              />
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Collapse
              unmountOnExit
              in={Boolean(dates.dateFrom && dates.dateTo && dates.dateFrom?.isAfter(dates.dateTo))}
            >
              <AlertThemed severity='error'>
                <AlertTitle>Error</AlertTitle>
                Incorrect time interval
              </AlertThemed>
            </Collapse>
          </Grid>
        </>
      </Grid>
    </LocalizationProvider>
  )
}
