import { type CreateTab, TAB_TYPE_LITERALS, createTabSchema } from 'Components/Dashboard/schemas'
import type { DashboardPanelV2 } from 'api/types'
import { useProjectInfo } from 'contexts/project'
import {
  Box,
  Button,
  MenuItem,
  TextField,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useForm, useWatch } from 'evidently-ui-lib/shared-dependencies/react-hook-form'
import { Form } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { zodResolver } from 'evidently-ui-lib/shared-dependencies/zod'
import { assertNever } from 'evidently-ui-lib/utils/index'
import { useIsAnyLoaderOrActionRunning } from 'hooks'
import { useLoader } from 'new-routes/hooks'
import { useEffect, useMemo } from 'react'
import invariant from 'tiny-invariant'
import { v7 as uuidv7 } from 'uuid'

export const CreateTabFormV2 = ({
  onSuccess,
  defaultValues
}: {
  onSuccess: ({ tab, newPanels }: { tab: CreateTab; newPanels: DashboardPanelV2[] }) => void
  defaultValues: CreateTab
}) => {
  const { project } = useProjectInfo()
  invariant(project, 'missing project')

  const { id: projectId } = project

  const {
    watch,
    control,
    setValue,
    setFocus,
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<CreateTab>({
    resolver: zodResolver(createTabSchema),
    defaultValues: defaultValues
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  const type = useWatch({ control, name: 'type' })

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useMemo(() => {
    if (type === 'Empty') {
      setValue('title', '', { shouldDirty: true })
    } else if (
      type === 'Data Quality' ||
      type === 'Columns' ||
      type === 'Data Drift' ||
      type === 'Descriptors'
    ) {
      setValue('title', type, { shouldDirty: true, shouldValidate: true })
    } else {
      assertNever(type)
    }
  }, [type])

  // focus on the firs input
  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => setFocus('title'), [])

  const metricsFetcher = useLoader('/v2/projects/:projectId/api/load-metrics')
  const allMetrics = metricsFetcher.data?.metrics ?? []

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (type !== 'Columns') {
      return
    }

    metricsFetcher.load({ paramsToReplace: { projectId }, query: { tags: JSON.stringify([]) } })
  }, [type])

  const meanMetricType = allMetrics.find((e) => e.includes('Mean'))
  const minMetricType = allMetrics.find((e) => e.includes('Min'))
  const maxMetricType = allMetrics.find((e) => e.includes('Max'))
  const uniqueMetricType = allMetrics.find((e) => e.includes('Unique'))

  const meanMetricColumnsFetcher = useLoader('/v2/projects/:projectId/api/load-label-values')

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (type !== 'Columns' || !meanMetricType) {
      return
    }

    meanMetricColumnsFetcher.load({
      paramsToReplace: { projectId },
      query: { tags: JSON.stringify([]), metric_type: meanMetricType, label: 'column' }
    })
  }, [type, meanMetricType])

  const meanColumns = meanMetricColumnsFetcher.data?.label_values ?? []

  const uniqueMetricColumnsFetcher = useLoader('/v2/projects/:projectId/api/load-label-values')

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (type !== 'Columns' || !uniqueMetricType) {
      return
    }

    uniqueMetricColumnsFetcher.load({
      paramsToReplace: { projectId },
      query: { tags: JSON.stringify([]), metric_type: uniqueMetricType, label: 'column' }
    })
  }, [type, uniqueMetricType])

  const uniqueColumns = uniqueMetricColumnsFetcher.data?.label_values ?? []

  return (
    <>
      <Typography align='center' variant='h4'>
        Create new tab
      </Typography>

      <Box maxWidth={600} p={3} mx={'auto'}>
        <Form
          onSubmit={handleSubmit((tab) => {
            if (tab.type === 'Empty') {
              onSuccess({ tab, newPanels: [] })
              return
            }

            if (tab.type === 'Data Drift') {
              onSuccess({ tab, newPanels: [] })
              return
            }

            if (tab.type === 'Data Quality') {
              onSuccess({ tab, newPanels: [] })
              return
            }

            if (tab.type === 'Columns') {
              if (meanMetricType && maxMetricType && minMetricType && uniqueMetricType) {
                onSuccess({
                  tab,
                  newPanels: [
                    ...generateMeanPanels({
                      columns: meanColumns,
                      meanMetric: meanMetricType,
                      maxMetric: maxMetricType,
                      minMetric: minMetricType
                    }),
                    ...generateUniquePanels({
                      columns: uniqueColumns,
                      uniqueMetric: uniqueMetricType
                    })
                  ]
                })
              }
              return
            }

            if (tab.type === 'Descriptors') {
              onSuccess({ tab, newPanels: [] })

              return
            }

            assertNever(tab.type)
          })}
        >
          <Box
            display={'flex'}
            alignItems={'flex-end'}
            justifyContent={'space-evenly'}
            columnGap={3}
          >
            {/* type */}
            <TextField
              sx={{ maxWidth: 150 }}
              variant='standard'
              size='small'
              label='Tab Template'
              select
              fullWidth
              value={type}
              {...register('type')}
            >
              {Object.values(TAB_TYPE_LITERALS)
                .filter((e) => e === 'Columns' || e === 'Empty')
                .map((option) => (
                  <MenuItem key={option} value={option}>
                    <Typography>{option}</Typography>
                  </MenuItem>
                ))}
            </TextField>

            {/* name */}
            <TextField
              {...register('title')}
              error={Boolean(errors.title)}
              helperText={errors.title?.message}
              variant='standard'
              label='Tab Name'
              InputLabelProps={{ shrink: Boolean(watch('title')) }}
            />

            {/* Submit button */}
            <Button
              disabled={
                isLoading ||
                // error here
                Object.keys(errors).length > 0
              }
              type='submit'
            >
              Submit
            </Button>
          </Box>
        </Form>
      </Box>
    </>
  )
}

const generateMeanPanels = ({
  columns,
  meanMetric,
  maxMetric,
  minMetric
}: {
  columns: string[]
  meanMetric: string
  maxMetric: string
  minMetric: string
}): DashboardPanelV2[] =>
  columns.map(
    (column_name) =>
      ({
        id: uuidv7(),
        size: 'full',
        title: column_name,
        plot_params: {
          plot_type: 'line'
        },
        values: [
          {
            metric: maxMetric,
            metric_labels: {
              column: column_name
            }
          },
          {
            metric: meanMetric,
            metric_labels: {
              column: column_name
            }
          },
          {
            metric: minMetric,
            metric_labels: {
              column: column_name
            }
          }
        ]
      }) satisfies DashboardPanelV2 as DashboardPanelV2
  )

const generateUniquePanels = ({
  columns,
  uniqueMetric
}: { columns: string[]; uniqueMetric: string }): DashboardPanelV2[] =>
  columns.map(
    (column_name) =>
      ({
        id: uuidv7(),
        size: 'full',
        title: column_name,
        plot_params: {
          plot_type: 'bar'
        },
        values: [
          {
            metric: uniqueMetric,
            metric_labels: {
              column: column_name,
              value_type: 'count'
            }
          }
        ]
      }) satisfies DashboardPanelV2 as DashboardPanelV2
  )
