import { useState } from 'react'

import { Box, Button, Grid, Link, TextField, Typography } from '@mui/material'

import {
  Link as RouterLink,
  LoaderFunctionArgs,
  useLoaderData,
  useParams,
  Outlet,
  useMatches,
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
import { Autocomplete } from '@mui/material'
import { useUpdateQueryStringValueWithoutNavigation } from 'hooks/useUpdateQueryStringValueWithoutNavigation'
import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid'
import dayjs from 'dayjs'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getReports(params.projectId)
}

export const action = async ({ params }: ActionFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.reloadProject(params.projectId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({ to: pathname, linkText: 'Reports' })
}

export const Component = () => {
  const { projectId } = useParams()

  const reports = useLoaderData() as loaderData
  const matches = useMatches()
  const submit = useSubmit()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  const showReportByIdMatch = matches.find(({ id }) => id === 'show-report-by-id')

  const ALL_TAGS = showReportByIdMatch
    ? [] // skip calculation in this case
    : // calculate unique tags
      Array.from(new Set(reports.flatMap(({ tags }) => tags)))

  const filteredReports = reports.filter(({ tags }) => {
    if (showReportByIdMatch) {
      return false
    }

    if (selectedTags.length === 0) {
      return true
    }

    return selectedTags.every((candidate) => tags.includes(candidate))
  })

  const rows: GridRowsProp = filteredReports.map((report) => ({
    id: report.id,
    'Report ID': report.id,
    tags: report.tags,
    timestamp: new Date(Date.parse(report.timestamp))
  }))

  const columns: GridColDef[] = [
    {
      field: 'Report ID',
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

  if (showReportByIdMatch) {
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
                Refresh Reports
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
