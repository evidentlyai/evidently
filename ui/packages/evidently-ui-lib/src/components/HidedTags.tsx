import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import { Box, Chip, IconButton } from '@mui/material'

import { useState } from 'react'

interface TagsProps {
  tags: string[]
  limitTags?: number
  onClick: (tag: string) => void
}

export const HidedTags = ({ onClick, tags, limitTags = 2 }: TagsProps) => {
  const [isShowFull, setShowFull] = useState(false)

  return (
    <Box display={'flex'} alignContent={'center'} flexWrap={'wrap'}>
      {tags.slice(0, limitTags).map((tag) => (
        <Chip onClick={() => onClick(tag)} key={tag} label={tag} style={{ margin: 3 }} />
      ))}
      {isShowFull &&
        tags
          .slice(limitTags)
          .map((tag) => (
            <Chip onClick={() => onClick(tag)} key={tag} label={tag} style={{ margin: 3 }} />
          ))}
      {!isShowFull && tags.length > limitTags && (
        <Chip
          variant='outlined'
          key='+N'
          label={`+${tags.length - limitTags}`}
          style={{ margin: 3, borderColor: 'grey' }}
          onClick={() => setShowFull(true)}
        />
      )}

      {tags.length > 0 && isShowFull && (
        <IconButton style={{ margin: 3 }} onClick={() => setShowFull(false)}>
          <CloseRoundedIcon fontSize='small' />
        </IconButton>
      )}
    </Box>
  )
}
