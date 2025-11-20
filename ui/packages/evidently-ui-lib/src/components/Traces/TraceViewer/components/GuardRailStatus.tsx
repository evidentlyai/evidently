import { Chip } from '@mui/material'

type GuardRailStatusProps = {
  guardRailStatus: string
}

export const GuardRailStatus = (props: GuardRailStatusProps) => {
  const { guardRailStatus } = props

  return (
    <Chip
      size='small'
      label={guardRailStatus}
      color={getGuardRailStatusColor(guardRailStatus)}
      variant={guardRailStatus === 'passed' ? 'outlined' : 'filled'}
    />
  )
}

export const getGuardRailStatusColor = (status: string) =>
  status === 'passed' ? 'success' : 'error'
