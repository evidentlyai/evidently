import { Close as CloseIcon } from '@mui/icons-material'
import {
  Box,
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  IconButton,
  Typography
} from '@mui/material'
import { useState } from 'react'
import { GenericTable } from '~/components/Table/GenericTable'
import type { GuardRailData } from '~/components/Traces/TraceViewer/utils'
import { GuardRailStatus } from './GuardRailStatus'

type GuardRailsShowInfoButtonProps = {
  guardRailData: GuardRailData[]
  onGoToSpan?: (spanId: string) => void
}

export const GuardRailsShowInfoButton = (props: GuardRailsShowInfoButtonProps) => {
  const { guardRailData, onGoToSpan } = props

  const allGuardRailDataCount = guardRailData.length
  const passedGuardRailDataCount = guardRailData.filter((entry) => entry.status === 'passed').length
  const failedGuardRailDataCount = guardRailData.filter((entry) => entry.status === 'failed').length

  const guardRailButtonInfoType =
    allGuardRailDataCount === passedGuardRailDataCount ? 'all-passed' : 'at-least-one-failed'

  const [isGuardRailDialogOpen, setIsGuardRailDialogOpen] = useState(false)

  if (guardRailData.length === 0) {
    return null
  }

  return (
    <>
      <Button
        size='small'
        color={guardRailButtonInfoType === 'all-passed' ? 'success' : 'error'}
        variant={guardRailButtonInfoType === 'all-passed' ? 'outlined' : 'contained'}
        onClick={() => setIsGuardRailDialogOpen(true)}
        disabled={allGuardRailDataCount === 0}
      >
        {guardRailButtonInfoType === 'all-passed'
          ? `${passedGuardRailDataCount}/${allGuardRailDataCount} passed`
          : `${failedGuardRailDataCount}/${allGuardRailDataCount} failed`}
      </Button>

      <Dialog
        open={isGuardRailDialogOpen}
        onClose={() => setIsGuardRailDialogOpen(false)}
        fullWidth
        PaperComponent={Box}
        slotProps={{
          paper: {
            sx: {
              backgroundColor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1
            }
          }
        }}
        maxWidth='md'
      >
        <DialogTitle>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant='h6'>Guard rails</Typography>
            <IconButton onClick={() => setIsGuardRailDialogOpen(false)} size='small'>
              <CloseIcon />
            </IconButton>
          </div>
        </DialogTitle>

        <DialogContent>
          <GenericTable
            data={guardRailData}
            idField='id'
            defaultSort={{ column: 'status', direction: 'asc' }}
            tableSize='small'
            removeLastBorderBottom
            columns={[
              {
                key: 'name',
                label: 'Name',
                sortable: { getSortValue: (row) => row.name },
                render: (row) => <Typography variant='body2'>{row.name}</Typography>
              },
              {
                key: 'status',
                label: 'Status',
                sortable: { getSortValue: (row) => row.status },
                align: 'right',
                render: (row) => <GuardRailStatus guardRailStatus={row.status} />
              },
              {
                key: 'error',
                label: 'Error',
                skipRender: failedGuardRailDataCount === 0,
                render: (row) => (
                  <Typography variant='body2' sx={{ whiteSpace: 'pre-wrap' }}>
                    {row.error ?? ''}
                  </Typography>
                )
              },
              {
                key: 'action',
                label: 'Action',
                align: 'right',
                skipRender: !onGoToSpan,
                minWidth: 150,
                render: (row) => (
                  <Button
                    size='small'
                    variant='outlined'
                    onClick={() => {
                      onGoToSpan?.(row.spanId)
                      setIsGuardRailDialogOpen(false)
                    }}
                  >
                    Go to span
                  </Button>
                )
              }
            ]}
          />
        </DialogContent>
      </Dialog>
    </>
  )
}
