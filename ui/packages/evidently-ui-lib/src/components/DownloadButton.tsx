import React from 'react'

import {
  Button,
  ClickAwayListener,
  Paper,
  Grow,
  Popper,
  MenuItem,
  MenuList,
  ButtonOwnProps
} from '@mui/material'

const options = [
  {
    title: 'Download HTML',
    format: 'html'
  },
  {
    title: 'Download JSON',
    format: 'json'
  }
]

export function DownloadButton(props: {
  downloadLink: string
  disabled: boolean
  variant?: ButtonOwnProps['variant']
}) {
  const [open, setOpen] = React.useState(false)
  const anchorRef = React.useRef<HTMLButtonElement>(null)

  const handleMenuItemClick = (downloadLink: string, format: string) => {
    window.open(`${downloadLink}?report_format=${format}`, '_blank')
    setOpen(false)
  }

  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen)
  }

  const handleClose = (event: MouseEvent | TouchEvent) => {
    if (anchorRef.current && anchorRef.current.contains(event.target as HTMLElement)) {
      return
    }

    setOpen(false)
  }

  return (
    <>
      <Button
        disabled={props.disabled}
        variant={props.variant}
        ref={anchorRef}
        color="primary"
        aria-controls={open ? 'split-button-menu' : undefined}
        aria-expanded={open ? 'true' : undefined}
        aria-label="select merge strategy"
        aria-haspopup="menu"
        onClick={handleToggle}
      >
        Download
      </Button>
      <Popper open={open} anchorEl={anchorRef.current} transition>
        {({ TransitionProps, placement }) => (
          <Grow
            {...TransitionProps}
            style={{
              transformOrigin: placement === 'bottom' ? 'center top' : 'center bottom'
            }}
          >
            <Paper>
              <ClickAwayListener onClickAway={handleClose}>
                <MenuList id="split-button-menu">
                  {options.map((option) => (
                    <MenuItem
                      key={option.format}
                      onClick={() => handleMenuItemClick(props.downloadLink, option.format)}
                    >
                      {option.title}
                    </MenuItem>
                  ))}
                </MenuList>
              </ClickAwayListener>
            </Paper>
          </Grow>
        )}
      </Popper>
    </>
  )
}
