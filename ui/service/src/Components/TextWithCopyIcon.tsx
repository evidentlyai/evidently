import IconButton from '@material-ui/core/IconButton'
import FilterNoneIcon from '@material-ui/icons/FilterNone'
import { Box } from '@material-ui/core'

export const TextWithCopyIcon = ({
  showText,
  copyText
}: {
  showText: string
  copyText: string
}) => {
  return (
    <Box>
      {showText}
      <IconButton
        size="small"
        style={{ marginLeft: 10 }}
        onClick={() => navigator.clipboard.writeText(copyText)}
      >
        <FilterNoneIcon fontSize="small" />
      </IconButton>
    </Box>
  )
}
