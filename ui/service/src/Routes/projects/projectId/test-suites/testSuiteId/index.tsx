import { RouteObject } from 'react-router-dom'
import SnapshotIdRoute from '../../_snapshotId'

export default {
  ...SnapshotIdRoute,
  id: 'show-test-suite-by-id'
} satisfies RouteObject
