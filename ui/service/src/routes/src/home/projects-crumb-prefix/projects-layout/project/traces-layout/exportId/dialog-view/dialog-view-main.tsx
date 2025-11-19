import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { Schemas } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { DialogViewer } from 'evidently-ui-lib/components/Traces/DialogViewer/index'
import { NameAndDescriptionPopover } from 'evidently-ui-lib/components/Utils/NameAndDescriptionForm'
import { useTraceToolbarRef } from 'evidently-ui-lib/contexts/TraceToolbarContext'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import {
  Autocomplete,
  Box,
  Button,
  Fade,
  Portal,
  Stack,
  TextField
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'
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

  return clientAPI
    .GET('/api/v1/traces/list', {
      params: { query: { export_id: exportId, getter_type: 'use_metadata_params_from_filters' } }
    })
    .then(responseParser())
    .then((traces) => ({
      name: traces.metadata.name,
      traces: traces.sessions,
      metadata: traces.metadata
    }))
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
        <Stack gap={2} direction={'row'} justifyContent={'center'} alignItems={'flex-end'}>
          <Box>
            <Box minWidth={180}>
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
                ListboxProps={{ sx: { maxHeight: 200 } }}
                options={['ungrouped', 'session', 'user']}
                renderInput={(params) => <TextField {...params} label={'Session splitting type'} />}
              />
            </Box>
          </Box>

          <Fade in={viewParams.session_type === 'session'} mountOnEnter unmountOnExit exit={false}>
            <Box>
              <TextField
                label={'Session Field'}
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
              <TextField
                label={'User ID Field'}
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
              <TextField
                label={'Dialog Split Time (sec)'}
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

          <Button
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
            Apply
          </Button>

          <Stack flex={1} direction={'row'} justifyContent={'flex-end'}>
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
        </Stack>
      </Portal>
      <Box>
        <Stack direction={'column'} gap={2}>
          <Box sx={[isStateNotSyncWithFilter && { opacity: 0.4 }]}>
            <Box my={3}>
              <DialogViewer
                key={exportId}
                data={data.traces}
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
        </Stack>
      </Box>
    </>
  )
}
