import { useState } from 'react'
import { useProjectFetcher } from '~/_routes/fetchers/project'
import { useIsAnyLoaderOrActionRunning, useOnSubmitEnd } from '~/_routes/hooks'

export const useProjectCardProps = () => {
  const projectFetcher = useProjectFetcher()

  const [mode, setMode] = useState<'edit' | 'view'>('view')

  const disabled = useIsAnyLoaderOrActionRunning()

  const onAlterMode = () => setMode((p) => (p === 'edit' ? 'view' : 'edit'))

  useOnSubmitEnd({
    state: projectFetcher.state,
    cb: () => projectFetcher.data === null && setMode('view')
  })

  return { mode, disabled, onAlterMode, projectFetcher }
}
