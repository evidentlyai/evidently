import { EvidentlyLogoSvg } from 'evidently-ui-lib/components/Icons/LogoSvg'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'

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
