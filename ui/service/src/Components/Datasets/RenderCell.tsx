import { useProjectInfo } from 'contexts/project'
import {
  RenderCell as RenderCellStandard,
  type SpecialColumnType
} from 'evidently-ui-lib/components/Datasets/hooks'
import { Tooltip, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { GridRenderCellParams } from 'evidently-ui-lib/shared-dependencies/mui-x-date-grid'
import { z } from 'evidently-ui-lib/shared-dependencies/zod'
import invariant from 'tiny-invariant'
import { LinkToTrace } from './LinkToTrace'

const uuidSchema = z.string().uuid()
const is_invalid_uuid = (s: string) => !s || !uuidSchema.safeParse(s).success

type RenderCellLinkToTraceProps = { value: string }

const RenderCellLinkToTrace = ({ value }: RenderCellLinkToTraceProps) => {
  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project

  const [exportId, traceId] = value.trim().split('/')

  if ([traceId, exportId].some(is_invalid_uuid)) {
    return (
      <Tooltip
        arrow
        placement='top'
        title={
          <Typography variant='caption'>
            In order to create link to trace you have to provide two uuids separated by a "/" as
            follows: <br /> {'"<export-uuid>/<trace-uuid>"'}
          </Typography>
        }
      >
        <Typography color='gray' fontStyle={'italic'}>
          incorrect format
        </Typography>
      </Tooltip>
    )
  }

  return (
    <LinkToTrace projectId={projectId} exportId={exportId} traceId={traceId} variant='outlined' />
  )
}

type RenderCellProps = { specialColumnType: SpecialColumnType } & GridRenderCellParams

export const RenderCell = ({ specialColumnType, ...props }: RenderCellProps) => {
  if (specialColumnType === 'link_to_trace') {
    return <RenderCellLinkToTrace value={String(props.value)} />
  }

  return <RenderCellStandard {...props} />
}
