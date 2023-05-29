import React from "react";
import ReactMarkdown from "react-markdown";

import {TextWidgetParams} from "../api/Api";
import Typography from "@material-ui/core/Typography";

const TextWidgetContent : React.FunctionComponent<TextWidgetParams> = (props) => {
    return (<>
        <Typography>
            <ReactMarkdown>{props.text}</ReactMarkdown>
        </Typography>
    </>);
}

export default TextWidgetContent;