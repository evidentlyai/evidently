import { IconButton, MenuItem, Popover, Select, useColorScheme } from '@mui/material'
import { useState } from 'react'

import DarkModeIcon from '@mui/icons-material/DarkMode'
import LightModeIcon from '@mui/icons-material/LightMode'
import { useThemeMode } from '~/hooks/theme'

export const ThemeToggle = () => {
  const { mode, setMode } = useColorScheme()
  const tMode = useThemeMode()
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null)

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) =>
    setAnchorEl(event.currentTarget)

  const handleClose = () => setAnchorEl(null)

  const open = Boolean(anchorEl)
  const id = open ? 'simple-popover' : undefined

  if (!mode) {
    return (
      <IconButton aria-describedby={id}>
        {tMode === 'dark' ? <DarkModeIcon /> : <LightModeIcon />}
      </IconButton>
    )
  }

  return (
    <div>
      <IconButton aria-describedby={id} onClick={handleClick}>
        {tMode === 'dark' ? <DarkModeIcon /> : <LightModeIcon />}
      </IconButton>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center'
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center'
        }}
      >
        <Select
          size={'small'}
          value={mode}
          onChange={(event) => {
            setMode(event.target.value as 'system' | 'light' | 'dark')
            handleClose()
          }}
        >
          <MenuItem value='system'>System</MenuItem>
          <MenuItem value='light'>Light</MenuItem>
          <MenuItem value='dark'>Dark</MenuItem>
        </Select>
      </Popover>
    </div>
  )
}
