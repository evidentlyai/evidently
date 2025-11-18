import { KeyboardArrowDown } from '@mui/icons-material'
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography
} from '@mui/material'
import { useState } from 'react'
import { TextWithCopyButton } from './TextWithCopyButton'

type AttributesViewerProps = {
  title: string
  data: Record<string, string | number | undefined>
}

export const AttributesViewer = (props: AttributesViewerProps) => {
  const { title, data } = props

  const [shown, setShown] = useState(false)
  const entries = Object.entries(data)

  let shortTitle = ''

  if (entries.length > 0) {
    const st = entries
      .slice(1)
      .reduce((prev, curr) => `${prev}  ${curr[0]}=${curr[1]}`, `${entries[0][0]}=${entries[0][1]}`)

    shortTitle = st.length < 150 ? st : `${st.slice(0, 150)}...`
  }

  return (
    <>
      <Accordion
        sx={{
          border: 'none',
          borderTop: '1px solid',
          borderColor: 'divider',
          '&::before': { display: 'none' }
        }}
        expanded={shown}
        onChange={(_, isExpanded) => setShown(isExpanded)}
        slotProps={{ transition: { unmountOnExit: true, mountOnEnter: true } }}
      >
        <AccordionSummary expandIcon={<KeyboardArrowDown />}>
          <Typography variant='body2' sx={{ '& .short-title': { color: 'text.disabled' } }}>
            {shown ? (
              <b>{title}</b>
            ) : (
              <span>
                <b>{title}</b> <span className='short-title'>{shortTitle}</span>
              </span>
            )}
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Table size={'small'}>
            <TableBody>
              {Object.entries(data).map(([k, v]) => (
                <TableRow
                  key={k}
                  sx={{
                    '&:nth-of-type(odd)': { backgroundColor: 'action.hover' },
                    '&:last-child td, &:last-child th': { border: 0 }
                  }}
                >
                  <TableCell width={'250px'} sx={{ fontSize: 14 }}>
                    {k}
                  </TableCell>
                  <TableCell sx={{ fontSize: 14 }}>
                    <TextWithCopyButton text={v?.toString()} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </AccordionDetails>
      </Accordion>
    </>
  )
}
