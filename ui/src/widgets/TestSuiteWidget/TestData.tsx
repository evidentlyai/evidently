import React, {useState} from "react";
import {TestData, TestState} from "../../api/Api";
import {Button, Collapse, Paper} from "@material-ui/core";
import {Alert, AlertTitle, Color} from "@material-ui/lab";
import {BigTableDetails} from "../BigTableWidget/BigTableDetails";
import ReactMarkdown from "react-markdown";


const availableStates: TestState[] = ["unknown", "success", "warning", "fail"];

export const StateToSeverity: (state: TestState) => Color = (state) => {
    switch (state) {
        case "error":
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
    const isDetailsAvailable = details !== undefined && details !== null && details.parts.length > 0;
    if (!availableStates.includes(state)) {
        console.error(`unexpected state: ${state} (expected one of [${availableStates.join(", ")}])`);
        state = "unknown";
    }
    return <><Paper>
        <Alert severity={StateToSeverity(state)}
               action={isDetailsAvailable ? <Button onClick={() => setDetailsPart(prev => ({active: !prev.active}))}
                               color="inherit" size="small">
                   Details
               </Button> : null }>
            <AlertTitle>{title}</AlertTitle>
            <ReactMarkdown>{description}</ReactMarkdown>
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