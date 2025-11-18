import { Paper, Table, TableBody, TableCell, TableRow } from '@mui/material'
import type { CostComponentProps } from './CostComponent'

export const CostTooltip = (props: CostComponentProps) => (
  <Paper
    elevation={2}
    sx={(t) => ({
      ...t.applyStyles('dark', { border: '1px solid', borderColor: 'divider' }),
      ...t.applyStyles('light', { boxShadow: t.shadows[5] })
    })}
  >
    <Table size={'small'} sx={{ '& tbody tr:last-child td': { borderBottom: 'none' } }}>
      <TableBody>
        {Array.from(props.breakdown.entries()).map((it) => (
          <TableRow key={it[0]}>
            <TableCell>{it[0]}</TableCell>
            <TableCell>{it[1][0]}</TableCell>
            {props.cost > 0 && <TableCell>{it[1][1] ? `$${it[1][1].toFixed(5)}` : ''}</TableCell>}
          </TableRow>
        ))}

        <TableRow>
          <TableCell sx={{ fontWeight: 'bold' }}>Total</TableCell>
          <TableCell sx={{ fontWeight: 'bold' }}>{props.tokens}</TableCell>
          {props.cost > 0 && (
            <TableCell sx={{ fontWeight: 'bold' }}>${props.cost.toFixed(5)}</TableCell>
          )}
        </TableRow>
      </TableBody>
    </Table>
  </Paper>
)
