import React, {useState} from "react";
import {TestData, TestState} from "../../api/Api";
import {Button, Collapse, Container, Grid, Paper, Typography} from "@material-ui/core";
import {Alert, AlertTitle, Color} from "@material-ui/lab";
import {BigTableDetails} from "../BigTableWidget/BigTableDetails";


const availableStates: TestState[] = ["unknown", "success", "warning", "fail"];

const stateToSeverity: (state: TestState) => Color = (state) => {
    switch (state) {
        case "unknown":
            return "info";
        case "success":
            return "success";
        case "warning":
            return "warning";
        case "fail":
            return "error";
    }
}

const TestData: React.FC<TestData> = ({title, description, state, details}) => {
    const [detailsPart, setDetailsPart] = useState({active: false});
    const isDetailsAvailable = details !== undefined;
    if (!availableStates.includes(state)) {
        console.error(`unexpected state: ${state} (expected one of [${availableStates.join(", ")}])`);
        state = "unknown";
    }
    return <><Paper>
        <Alert severity={stateToSeverity(state)}
               action={isDetailsAvailable ? <Button onClick={() => setDetailsPart(prev => ({active: !prev.active}))}
                               color="inherit" size="small">
                   Details
               </Button> : null }>
            <AlertTitle>{title}</AlertTitle>
            {description}
        </Alert>
        {!isDetailsAvailable ? <></> :
            <Collapse in={detailsPart.active} mountOnEnter={true} unmountOnExit={true}>
                <Paper style={{padding: "2px"}}>
                    <BigTableDetails details={details!} widgetSize={2}/>
                </Paper>
            </Collapse>}
    </Paper></>
}

export default TestData;