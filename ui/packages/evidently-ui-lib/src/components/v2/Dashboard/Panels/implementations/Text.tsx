import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { PanelCardGeneral } from './helpers/general'

export type TextPanelProps = MakePanel<{
  type: 'text'
  size: 'full' | 'half'
  title?: string
  description?: string
}>

export const TextDashboardPanel = ({ title, description }: TextPanelProps) => {
  return (
    <>
      <PanelCardGeneral
        title={title}
        description={description}
        sxCardContent={{ p: '16px !important' }}
        textCenterAlign
      />
    </>
  )
}
