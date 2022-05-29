import React from "react";
import {TestSuiteWidgetParams} from "../../api/Api";
import TestData from "./TestData";
import {Grid} from "@material-ui/core";

/**
 * render whole Test Suite block in Dashboard view
 * @constructor
 */
const TestSuiteWidgetContent : React.FC<TestSuiteWidgetParams> = ({tests}) =>
    (<><Grid container spacing={2}>
        {tests.map(test => <Grid item xs={12}><TestData {...test} /></Grid>)}
        </Grid>
    </>)

export default TestSuiteWidgetContent;