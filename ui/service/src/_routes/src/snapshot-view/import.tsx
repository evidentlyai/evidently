// export * as SnapshotId from '~/_routes/src/snapshot-view/snapshot-view-main'

// we export it lazy because of ~2.6 MB chunk size :) plotly.js is too big :3
const lazy = () => import('~/_routes/src/snapshot-view/snapshot-view-main')
export const SnapshotIdLazy = { lazy } as const
