import { Table, TableBody, TableCell, TableRow, Typography } from '@mui/material'
import { TextWithCopyButton } from './TextWithCopyButton'

type AttributesViewerProps = {
  data: Record<string, string | number | undefined>
  alterBackgroundOdd: boolean
}

export const AttributesViewer = (props: AttributesViewerProps) => {
  const { data, alterBackgroundOdd } = props

  return (
    <>
      <Table size='small'>
        <TableBody>
          {Object.entries(data).map(([k, v]) => (
            <TableRow
              key={k}
              sx={[
                alterBackgroundOdd && {
                  '&:nth-of-type(odd)': { backgroundColor: 'divider' }
                }
              ]}
            >
              <TableCell>
                <Typography>{k}</Typography>
              </TableCell>
              <TableCell>
                <TextWithCopyButton text={String(v)} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}
