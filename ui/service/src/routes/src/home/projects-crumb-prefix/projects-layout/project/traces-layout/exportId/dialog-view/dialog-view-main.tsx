import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { Schemas } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { FeedbackForm } from 'evidently-ui-lib/components/HumanFeedback/FeedbackForm'
import {
  TraceHeader,
  TraceIdDisplay
} from 'evidently-ui-lib/components/Traces/DialogViewer/components/TraceHeader'
import { DialogViewer } from 'evidently-ui-lib/components/Traces/DialogViewer/index'
import { extractFeedbackData } from 'evidently-ui-lib/components/Traces/TraceViewer/utils'
import { NameAndDescriptionPopover } from 'evidently-ui-lib/components/Utils/NameAndDescriptionForm'
import { useTraceToolbarRef } from 'evidently-ui-lib/contexts/TraceToolbarContext'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { ArrowForward as ArrowForwardIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { Close as CloseIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { IconButton } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  Autocomplete,
  Box,
  Button,
  Divider,
  Fade,
  Portal,
  Stack,
  TextField,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'
import { LinkToTrace } from '~/Components/Datasets/LinkToTrace'
import { clientAPI } from '~/api'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces/:exportId/dialog'

type CurrentRouteParams = GetParams<typeof currentRoutePath>
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = {
  keyFromLoaderData: 'name' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { exportId } = params as CurrentRouteParams

  const metadataPromise = clientAPI
    .GET('/api/datasets/{dataset_id}/metadata', {
      params: { path: { dataset_id: exportId } }
    })
    .then(responseParser())

  const dataPromise = clientAPI
    .GET('/api/v1/traces/list', {
      params: { query: { export_id: exportId, getter_type: 'with_filters_from_metadata' } }
    })
    .then(responseParser())

  const [metadata, data] = await Promise.all([metadataPromise, dataPromise])

  return {
    name: data.metadata.name,
    traces: data.sessions,
    metadata: data.metadata,
    human_feedback_custom_shortcut_labels: metadata.human_feedback_custom_shortcut_labels
  }
}

export const actions = {
  'update-tracing-session-params': async (
    args: ActionArgs<{ data: Schemas['DatasetTracingParams'] }>
  ) => {
    const { data, params } = args

    const { exportId } = params as CurrentRouteParams

    const response = await clientAPI
      .POST('/api/v1/traces/metadata', {
        params: { query: { export_id: exportId } },
        body: data
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(response)) {
      return response
    }

    return null
  }
}

///////////////////
//  COMPONENT
///////////////////

export const Component = () => {
  const { loaderData: data, params } = useCurrentRouteParams<CurrentRoute>()

  const { exportId, projectId } = params

  const traceToolbarRef = useTraceToolbarRef()

  const defaultValues = {
    input_attribute: data.metadata.params?.user_message_field ?? '',
    output_attribute: data.metadata.params?.assistant_message_field ?? '',
    session_type: data.metadata.params?.session_type ?? 'ungrouped',
    session_attribute: data.metadata.params?.session_field ?? 'session_id',
    user_id_attribute: data.metadata.params?.user_field ?? 'user_id',
    split_time_seconds: data.metadata.params?.dialog_split_time_seconds?.toString() ?? '1800'
  }

  const [viewParams, setViewParams] = useState({ ...defaultValues })

  const [feedbackTraceId, setFeedbackTraceId] = useState<string | null>(null)

  const selectedTraceForFeedback = Object.values(data.traces)
    .flat()
    .find((t) => t.trace_id === feedbackTraceId)

  const defaultFeedbackData = extractFeedbackData(selectedTraceForFeedback)

  const additionalLabels = data.human_feedback_custom_shortcut_labels ?? []

  const sessions = Object.keys(data.traces)
  const isAFewSessions = Boolean(!(sessions.length === 1) && sessions.length > 0 ? sessions[0] : '')

  const isCanCreateDataset = Boolean(
    viewParams.session_type === 'session' &&
      viewParams.input_attribute &&
      viewParams.output_attribute &&
      viewParams.session_attribute &&
      isAFewSessions
  )

  const isLoading = useIsAnyLoaderOrActionRunning()

  const exportToDatasetFetcher = useSubmitFetcher({
    path: '/projects/:projectId/datasets',
    action: 'export-to-dataset-from-source-and-redirect-to-dataset'
  })

  const updateDatasetMetadataFetcher = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId/dialog',
    action: 'update-tracing-session-params'
  })

  const editTraceFeedbackFetcher = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId',
    action: 'edit-trace-feedback'
  })

  const editTraceFeedbackCustomShortcutLabelsFetcher = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId',
    action: 'edit-trace-feedback-custom-shortcut-labels'
  })

  const isStateNotSyncWithFilter = !(
    viewParams.session_type === defaultValues.session_type &&
    viewParams.session_attribute === defaultValues.session_attribute &&
    viewParams.split_time_seconds === defaultValues.split_time_seconds &&
    viewParams.user_id_attribute === defaultValues.user_id_attribute
  )

  const isMessageFieldsChanged = !(
    viewParams.input_attribute === defaultValues.input_attribute &&
    viewParams.output_attribute === defaultValues.output_attribute
  )

  return (
    <>
      <Portal container={() => traceToolbarRef.current}>
        <Stack
          gap={2}
          direction={'row'}
          justifyContent={'center'}
          alignItems={'flex-end'}
          border={1}
          borderColor='divider'
          borderRadius={1}
          p={2}
        >
          <Box>
            <Box minWidth={180}>
              <Typography variant='subtitle2' gutterBottom>
                Session splitting type
              </Typography>

              <Autocomplete
                fullWidth
                size='small'
                getOptionLabel={(x) => x}
                getOptionKey={(x) => x}
                onChange={(_, value) => {
                  if (value) {
                    setViewParams((prev) => ({ ...prev, session_type: value }))
                  }
                }}
                value={viewParams.session_type}
                options={['ungrouped', 'session', 'user']}
                renderInput={(params) => <TextField {...params} />}
              />
            </Box>
          </Box>

          <Fade in={viewParams.session_type === 'session'} mountOnEnter unmountOnExit exit={false}>
            <Box>
              <Typography variant='subtitle2' gutterBottom>
                Session Field
              </Typography>

              <TextField
                name='session_attribute'
                size={'small'}
                defaultValue={viewParams.session_attribute}
                onChange={(e) =>
                  setViewParams((prev) => ({ ...prev, session_attribute: e.target.value }))
                }
              />
            </Box>
          </Fade>

          <Fade in={viewParams.session_type === 'user'} mountOnEnter unmountOnExit exit={false}>
            <Box>
              <Typography variant='subtitle2' gutterBottom>
                User ID Field
              </Typography>

              <TextField
                name='user_id_attribute'
                size={'small'}
                defaultValue={viewParams.user_id_attribute}
                onChange={(e) => {
                  setViewParams((prev) => ({ ...prev, user_id_attribute: e.target.value }))
                }}
              />
            </Box>
          </Fade>

          <Fade in={viewParams.session_type === 'user'} mountOnEnter unmountOnExit exit={false}>
            <Box>
              <Typography variant='subtitle2' gutterBottom>
                Dialog Split Time (sec)
              </Typography>

              <TextField
                slotProps={{ htmlInput: { min: 1 } }}
                name='split_time_seconds'
                type='number'
                size={'small'}
                defaultValue={viewParams.split_time_seconds}
                onChange={(e) => {
                  setViewParams((prev) => ({ ...prev, split_time_seconds: e.target.value }))
                }}
              />
            </Box>
          </Fade>

          <Divider orientation='vertical' flexItem />

          <Button
            size='small'
            disabled={!isStateNotSyncWithFilter && !isMessageFieldsChanged}
            variant='outlined'
            onClick={() => {
              updateDatasetMetadataFetcher.submit({
                data: {
                  user_field: viewParams.user_id_attribute,
                  user_message_field: viewParams.input_attribute,
                  session_type: viewParams.session_type,
                  session_field: viewParams.session_attribute,
                  assistant_message_field: viewParams.output_attribute,
                  dialog_split_time_seconds:
                    typeof viewParams.split_time_seconds === 'number'
                      ? viewParams.split_time_seconds
                      : Number.parseInt(viewParams.split_time_seconds)
                },
                paramsToReplace: { projectId, exportId }
              })
            }}
          >
            Apply filters
          </Button>

          <NameAndDescriptionPopover
            buttonDisabled={isStateNotSyncWithFilter || !isCanCreateDataset || isLoading}
            formProps={{
              allowSubmitDefaults: true,
              submitButtonTitle: 'Submit',
              defaultValues: { name: `Export of ${data.name}` },
              isLoading: exportToDatasetFetcher.state !== 'idle',
              onSubmit: ({ name, description }) => {
                const [spanName] = viewParams.input_attribute.split(':')

                exportToDatasetFetcher.submit({
                  data: {
                    name,
                    description,
                    source: {
                      type: 'evidently:data_source_dto:TracingSessionDataSourceDTO',
                      export_id: exportId,
                      session_id_column: `${spanName}:${viewParams.session_attribute}`.replaceAll(
                        ':',
                        '.'
                      ),
                      question_column: viewParams.input_attribute.replaceAll(':', '.'),
                      response_column: viewParams.output_attribute.replaceAll(':', '.'),
                      timestamp_column: 'timestamp'
                    }
                  },
                  paramsToReplace: { projectId }
                })
              }
            }}
            buttonTitle='Export to Dataset'
          />
        </Stack>
      </Portal>

      <Box
        display='grid'
        gridTemplateColumns={feedbackTraceId ? '65% 35%' : '100% 0'}
        sx={{ transition: '325ms ease-in-out' }}
      >
        <Box>
          <Box sx={[isStateNotSyncWithFilter && { opacity: 0.4 }]}>
            <Box my={3}>
              <DialogViewer
                key={exportId}
                data={data.traces}
                traceHeader={({ trace }) => (
                  <TraceHeader
                    traceId={trace.trace_id}
                    feedback={{
                      isEditing: feedbackTraceId === trace.trace_id,
                      label: extractFeedbackData(trace).label,
                      comment: extractFeedbackData(trace).comment,
                      onEdit: () => setFeedbackTraceId(trace.trace_id)
                    }}
                    additionalComponents={
                      <LinkToTrace
                        size='small'
                        title='Go to trace'
                        variant='outlined'
                        endIcon={<ArrowForwardIcon />}
                        exportId={exportId}
                        projectId={projectId}
                        traceId={trace.trace_id}
                      />
                    }
                  />
                )}
                description={{
                  inputAttribute: viewParams.input_attribute,
                  setInputAttribute: (state) => {
                    setViewParams((prev) => ({
                      ...prev,
                      input_attribute:
                        typeof state === 'function' ? state(prev.input_attribute) : state
                    }))
                  },
                  outputAttribute: viewParams.output_attribute,
                  setOutputAttribute: (state) => {
                    setViewParams((prev) => ({
                      ...prev,
                      output_attribute:
                        typeof state === 'function' ? state(prev.output_attribute) : state
                    }))
                  },
                  sessionAttribute: viewParams.session_attribute,
                  userIdAttribute: viewParams.user_id_attribute,
                  splitTime: Number.parseInt(viewParams.split_time_seconds)
                }}
              />
            </Box>
          </Box>
        </Box>

        <Fade in={Boolean(feedbackTraceId)} timeout={800}>
          <Box borderLeft={1} borderColor='divider' p={2}>
            {feedbackTraceId && (
              <Box position='sticky' top={10} right={0}>
                <Stack gap={2}>
                  <Stack direction='row' alignItems='center' justifyContent='space-between'>
                    <Typography variant='h5'>Feedback</Typography>

                    <IconButton onClick={() => setFeedbackTraceId(null)} size='small'>
                      <CloseIcon />
                    </IconButton>
                  </Stack>

                  <TraceIdDisplay traceId={feedbackTraceId ?? ''} />

                  <FeedbackForm
                    key={feedbackTraceId}
                    buttonText='Save'
                    evaluationZero
                    defaultFeedbackData={defaultFeedbackData}
                    onSubmitFeedbackData={(data) => {
                      editTraceFeedbackFetcher.submit({
                        data: {
                          traceId: feedbackTraceId,
                          label: data.label,
                          comment: data.comment
                        },
                        paramsToReplace: { projectId, exportId }
                      })
                    }}
                    submitDisabled={editTraceFeedbackFetcher.state !== 'idle'}
                    additionalLabels={additionalLabels}
                    setAdditionalLabels={(labels) => {
                      editTraceFeedbackCustomShortcutLabelsFetcher.submit({
                        data: { human_feedback_custom_shortcut_labels: labels },
                        paramsToReplace: { projectId, exportId }
                      })
                    }}
                    additionalLabelsDisabled={
                      editTraceFeedbackCustomShortcutLabelsFetcher.state !== 'idle'
                    }
                  />
                </Stack>
              </Box>
            )}
          </Box>
        </Fade>
      </Box>
    </>
  )
}
