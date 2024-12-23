// export * as SnapshotId from '~/routes/src/snapshot-view/snapshot-view-main'

// we export it lazy because of ~2.6 MB chunk size :) plotly.js is too big :3
const lazy = () => import('./snapshot-view-main')
export const SnapshotIdLazy = { lazy } as const
