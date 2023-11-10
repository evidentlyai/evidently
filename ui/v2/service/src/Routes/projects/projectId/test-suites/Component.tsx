import { Box, Button, Grid, Link, TextField, Typography } from '@mui/material'
import {
  Link as RouterLink,
  LoaderFunctionArgs,
  useLoaderData,
  useParams,
  useMatches,
  Outlet,
  useSearchParams,
  ActionFunctionArgs,
  useSubmit
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { TextWithCopyIcon } from 'Components/TextWithCopyIcon'
import { DownloadButton } from 'Components/DownloadButton'
import { HidedTags } from 'Components/HidedTags'
import { crumbFunction } from 'Components/BreadCrumbs'
import { useUpdateQueryStringValueWithoutNavigation } from 'hooks/useUpdateQueryStringValueWithoutNavigation'
import { useState } from 'react'
import { Autocomplete } from '@mui/material'
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid'
import dayjs from 'dayjs'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getTestSuites(params.projectId)
}

export const action = async ({ params }: ActionFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.reloadProject(params.projectId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({ to: pathname, linkText: 'Test Suites' })
}

export const Component = () => {
  const { projectId } = useParams()
  const testSuites = useLoaderData() as loaderData
  const matches = useMatches()
  const submit = useSubmit()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  const showTestSuiteByIdMatch = matches.find(({ id }) => id === 'show-test-suite-by-id')

  const ALL_TAGS = showTestSuiteByIdMatch
    ? [] // skip calculation in this case
    : // calculate unique tags
      Array.from(new Set(testSuites.flatMap(({ tags }) => tags)))

  const filteredTestSuites = testSuites.filter(({ tags }) => {
    if (showTestSuiteByIdMatch) {
      return false
    }

    if (selectedTags.length === 0) {
      return true
    }

    return selectedTags.every((candidate) => tags.includes(candidate))
  })

  const rows: GridRowsProp = filteredTestSuites.map((testSuite) => ({
    id: testSuite.id,
    'Test Suite ID': testSuite.id,
    tags: testSuite.tags,
    timestamp: new Date(Date.parse(testSuite.timestamp))
  }))

  const columns: GridColDef[] = [
    {
      field: 'Test Suite ID',
      flex: 2,
      sortable: false,
      renderCell: ({ row }) => {
        return (
          <Box minHeight={73} display={'flex'} alignItems={'center'}>
            <TextWithCopyIcon showText={row.id} copyText={row.id} />
          </Box>
        )
      }
    },
    {
      field: 'Tags',
      flex: 2,
      sortable: false,
      renderCell: ({ row }) => {
        return (
          <Box p={2}>
            <HidedTags
              onClick={(clickedTag) => {
                if (selectedTags.includes(clickedTag)) {
                  return
                }

                setTags([...selectedTags, clickedTag])
              }}
              tags={row.tags}
            />
          </Box>
        )
      }
    },
    {
      field: 'timestamp',
      type: 'dateTime',
      flex: 1,
      renderCell({ row }) {
        return (
          <Typography variant="body2">
            {dayjs(row.timestamp).locale('en-gb').format('llll')}
          </Typography>
        )
      }
    },
    {
      field: 'Actions',
      flex: 1,
      sortable: false,
      renderCell({ row }) {
        return (
          <>
            <Link component={RouterLink} to={`${row.id}`}>
              <Button>View</Button>
            </Link>
            <DownloadButton downloadLink={`/api/projects/${projectId}/${row.id}/download`} />
          </>
        )
      }
    }
  ]

  if (showTestSuiteByIdMatch) {
    return (
      <Grid container>
        <Grid item xs={12}>
          <Outlet />
        </Grid>
      </Grid>
    )
  }

  return (
    <>
      <Box sx={{ padding: 2 }}>
        <Grid container spacing={2} alignItems={'end'}>
          <Grid item xs={12} md={6}>
            <Autocomplete
              multiple
              limitTags={2}
              value={selectedTags}
              onChange={(_, newSelectedTags) => setTags(newSelectedTags)}
              options={ALL_TAGS}
              renderInput={(params) => (
                <TextField {...params} variant="standard" label="Filter by Tags" />
              )}
            />
          </Grid>
          <Grid item flexGrow={2}>
            <Box display="flex" justifyContent="flex-end">
              <Button
                variant="outlined"
                onClick={() => submit(null, { method: 'post' })}
                color="primary"
              >
                Refresh Test Suites
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Box>

      <DataGrid
        sx={{
          border: 'none',
          [['.MuiDataGrid-cell', '.MuiDataGrid-columnHeader']
            .flatMap((e) => [e + ':focus', e + ':focus-within'])
            .join(', ')]: { outline: 'unset' }
        }}
        initialState={{
          sorting: {
            sortModel: [{ field: 'timestamp', sort: 'desc' }]
          }
        }}
        disableRowSelectionOnClick
        disableColumnMenu
        getRowHeight={() => 'auto'}
        density="standard"
        columns={columns}
        rows={rows}
      />
    </>
  )
}
