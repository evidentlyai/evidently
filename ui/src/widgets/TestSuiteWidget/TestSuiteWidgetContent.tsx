import React, {useState} from "react";
import {TestSuiteWidgetParams, TestData, TestGroupData, TestGroupTypeData} from "../../api/Api";
import TestInfo, {StateToSeverity} from "./TestData";
import {Button, Collapse, Grid, MenuItem, Paper, Select} from "@material-ui/core";
import {Alert, AlertTitle} from "@material-ui/lab";


type TestSuiteFoldingProps = {
    type: string,
    availableTypes: TestGroupTypeData[],
    onChange: (newType: string) => void
};
const TestSuiteFolding: React.FC<TestSuiteFoldingProps> = ({type, availableTypes, onChange}) =>
    (
        <>
            <Select value={type} onChange={event => onChange(event.target.value as string)}>
                {availableTypes.map(typeData => <MenuItem value={typeData.id}>{typeData.title}</MenuItem>)}
            </Select>
        </>
    )


const TestGroup: React.FC<{ groupInfo: TestGroupData, tests: TestData[] }> = ({groupInfo, tests}) => {
    const [collapse, setCollapse] = useState({active: false});
    return <><Paper>
        <Alert severity={StateToSeverity(groupInfo.severity ?? "unknown")}
               action={<Button onClick={() => setCollapse(prev => ({active: !prev.active}))} color="inherit"
                               size="small">
                   {collapse.active ? "Hide" : "Show"}
               </Button>}>
            <AlertTitle>{groupInfo.title}</AlertTitle>
            {groupInfo.description}
        </Alert>
        <Collapse in={collapse.active} mountOnEnter={true} unmountOnExit={true}>
            <Grid container spacing={2}>
                {tests.map(test => <Grid item xs={12}><TestInfo {...test} /></Grid>)}
            </Grid>
        </Collapse>
    </Paper></>
}


type GroupedSectionProps = {
    type: string,
    groupsInfo: TestGroupTypeData[],
    tests: TestData[],
};

const GroupedSection: React.FC<GroupedSectionProps> = ({type, groupsInfo, tests}) => {
    function getGroupFn(type: string): [TestGroupData[], (test: TestData) => string] {
        if (type === "status") {
            return [groupsInfo.find(t => t.id === type)!.values, test => test.state]
        }

        throw "unexpected type";
    }

    const [actualGroups, groupFn] = getGroupFn(type)
    const grouped = tests.reduce((agg, curr) => {
        agg.set(groupFn(curr), [...(agg.get(groupFn(curr)) ?? []), curr]);
        return agg;
    }, new Map<string, TestData[]>())

    return <>
        <Grid container spacing={2}>
            {Array.from(grouped.entries())
                .map(([key, value]) => [actualGroups.find(t => t.id === key)!, value] as [TestGroupData, TestData[]])
                .sort((a, b) => a[0].sortIndex - b[0].sortIndex)
                .map(([key, value]) =>
                    <Grid item xs={12}>
                        <TestGroup groupInfo={key} tests={value}/>
                    </Grid>)
            }
        </Grid>
    </>
}

const DefaultGroups: TestGroupTypeData[] = [
    {id: "none", title: "No Grouping", values: []},
    {id: "status", title: "Status", values: [
    {id: "success", title: "Passed tests", sortIndex: 3, description: "", severity: "success"},
    {id: "fail", title: "Failed tests", sortIndex: 1, description: "", severity: "fail"},
    {id: "warning", title: "Passed tests with warnings", sortIndex: 2, description: "", severity: "warning"},
]},
]

/**
 * render whole Test Suite block in Dashboard view
 * @constructor
 */
const TestSuiteWidgetContent: React.FC<TestSuiteWidgetParams> = ({tests, testGroupTypes}) => {
    const [grouping, changeGrouping] = React.useState({"group_type": "none"})
    return (<><Grid container spacing={2}>
        <Grid item xs={12}>
            <TestSuiteFolding type={grouping.group_type}
                              availableTypes={[...DefaultGroups, ...(testGroupTypes ?? [])]}
                              onChange={type => changeGrouping({"group_type": type})}/>
        </Grid>
        <Grid item xs={12}>
            <Grid container spacing={2}>
                {grouping.group_type === "none"
                    ? tests.map(test => <Grid item xs={12}><TestInfo {...test} /></Grid>)
                    : <GroupedSection type={grouping.group_type}
                                      groupsInfo={testGroupTypes}
                                      tests={tests}/>}
            </Grid>
        </Grid>
    </Grid>
    </>);
}

export default TestSuiteWidgetContent;