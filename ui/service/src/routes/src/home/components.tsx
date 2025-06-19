import { EvidentlyLogoSvg } from 'evidently-ui-lib/components/LogoSvg'
import { RouterLink } from '~/routes/components'

export const HomeLink = () => (
  <RouterLink
    type='icon'
    to='/'
    IconButtonProps={{
      children: <EvidentlyLogoSvg />,
      sx: (theme) => ({
        color: '#4d4d4d',
        ...theme.applyStyles('dark', {
          color: 'text.primary'
        }),
        '&:hover': {
          borderRadius: '5px',
          color: 'text.secondary'
        }
      })
    }}
  />
)
