import { Box, Button, Collapse, Grid, Select } from '@mui/material'
import { Alert, AlertTitle } from '@mui/material'
import React, { useState } from 'react'
import type { TestDataInfo, TestGroupData, TestGroupTypeData, TestSuiteWidgetParams } from '~/api'
import TestInfo, { StateToSeverity } from './TestData'

type TestSuiteFoldingProps = {
  type: string
  availableTypes: TestGroupTypeData[]
  onChange: (newType: string) => void
}
const TestSuiteFolding: React.FC<TestSuiteFoldingProps> = ({ type, availableTypes, onChange }) => (
  <>
    <Select
      variant='standard'
      value={type}
      onChange={(event) => onChange(event.target.value as string)}
      native={true}
    >
      {availableTypes.map((typeData) => (
        <option key={typeData.id} value={typeData.id}>
          {typeData.title}
        </option>
      ))}
    </Select>
  </>
)

const TestGroup: React.FC<{ groupInfo: TestGroupData; tests: TestDataInfo[] }> = ({
  groupInfo,
  tests
}) => {
  const [collapse, setCollapse] = useState({ active: false })
  return (
    <>
      <Box mt={2} px={2}>
        <Alert
          severity={StateToSeverity(groupInfo.severity ?? 'unknown')}
          icon={false}
          action={
            <Button
              onClick={() => setCollapse((prev) => ({ active: !prev.active }))}
              color='inherit'
              size='small'
            >
              {collapse.active ? 'Hide' : 'Show'}
            </Button>
          }
        >
          <AlertTitle>{groupInfo.title}</AlertTitle>
          {groupInfo.description}
        </Alert>
        <Collapse in={collapse.active} mountOnEnter={true} unmountOnExit={true}>
          <Grid container spacing={2} style={{ padding: 10, paddingTop: 20 }}>
            {tests.map((test) => (
              // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
              <Grid item xs={12}>
                <TestInfo {...test} />
              </Grid>
            ))}
          </Grid>
        </Collapse>
      </Box>
    </>
  )
}

type GroupedSectionProps = {
  type: string
  groupsInfo: TestGroupTypeData[]
  tests: TestDataInfo[]
}

const GroupedSection: React.FC<GroupedSectionProps> = ({ type, groupsInfo, tests }) => {
  function getGroupFn(type: string): [TestGroupData[], (test: TestDataInfo) => string] {
    if (type === 'status') {
      // biome-ignore lint: <explanation>
      return [groupsInfo.find((t) => t.id === type)!.values, (test) => test.state]
    }

    const group = groupsInfo.find((t) => t.id === type)
    if (group === undefined) {
      throw 'unexpected type'
    }
    const groups =
      group.values.find((v) => v.id === 'no group') !== undefined
        ? group.values
        : [
            ...group.values,
            {
              id: 'no group',
              title: 'No Group',
              sortIndex: -1,
              description: 'No group of this type was provided'
            }
          ]
    return [groups, (test) => test.groups[type] ?? 'no group']
  }

  const [actualGroups, groupFn] = getGroupFn(type)
  const grouped = tests.reduce((agg, curr) => {
    agg.set(groupFn(curr), [...(agg.get(groupFn(curr)) ?? []), curr])
    return agg
  }, new Map<string, TestDataInfo[]>())

  return (
    <>
      <Grid container spacing={2}>
        {Array.from(grouped.entries())
          .map(
            ([key, value]) =>
              [
                actualGroups.find((t) => t.id === key) ?? {
                  id: key,
                  title: key
                },
                value
              ] as [TestGroupData, TestDataInfo[]]
          )
          .sort((a, b) => (a[0].sortIndex ?? 0) - (b[0].sortIndex ?? 0))
          .map(([key, value]) => (
            // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
            <Grid item xs={12}>
              <TestGroup groupInfo={key} tests={value} />
            </Grid>
          ))}
      </Grid>
    </>
  )
}

const DefaultGroups: TestGroupTypeData[] = [
  { id: 'none', title: 'All tests', values: [] },
  {
    id: 'status',
    title: 'By test status',
    values: [
      { id: 'success', title: 'Passed tests', sortIndex: 3, description: '', severity: 'success' },
      { id: 'fail', title: 'Failed tests', sortIndex: 1, description: '', severity: 'fail' },
      {
        id: 'warning',
        title: 'Failed non-critical tests',
        sortIndex: 2,
        description: '',
        severity: 'warning'
      },
      {
        id: 'error',
        title: 'Tests with execution errors',
        sortIndex: 2,
        description: '',
        severity: 'error'
      }
    ]
  }
]

/**
 * render whole Test Suite block in Dashboard view
 * @constructor
 */
const TestSuiteWidgetContent: React.FC<TestSuiteWidgetParams> = ({ tests, testGroupTypes }) => {
  const [grouping, changeGrouping] = React.useState({ group_type: 'none' })
  const existingGroupTypes: string[] = []
  for (let i = 0; i < tests.length; i++) {
    const test = tests[i]
    const keys = Object.keys(test.groups)
    for (const key of keys) {
      if (existingGroupTypes.findIndex((k) => k === key) === -1) {
        existingGroupTypes.push(key)
      }
    }
  }
  const availableTypes = [
    ...DefaultGroups,
    ...(testGroupTypes ?? []).filter((t) => existingGroupTypes.findIndex((k) => k === t.id) !== -1)
  ]

  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TestSuiteFolding
            type={grouping.group_type}
            availableTypes={availableTypes}
            onChange={(type) => changeGrouping({ group_type: type })}
          />
        </Grid>
        <Grid item xs={12}>
          <Grid container spacing={2}>
            {grouping.group_type === 'none' ? (
              tests.map((test) => (
                <Grid item key={test.title + test.description} xs={12}>
                  <TestInfo {...test} />
                </Grid>
              ))
            ) : (
              <GroupedSection
                type={grouping.group_type}
                groupsInfo={availableTypes}
                tests={tests}
              />
            )}
          </Grid>
        </Grid>
      </Grid>
    </>
  )
}

export default TestSuiteWidgetContent
