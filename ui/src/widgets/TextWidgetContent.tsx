import React from "react";
import ReactMarkdown from "react-markdown";

import {TextWidgetParams} from "../api/Api";

const TextWidgetContent : React.FunctionComponent<TextWidgetParams> = (props) => {
    console.log(props)
    return (<>
        <ReactMarkdown>{props.text}</ReactMarkdown>
    </>);
}

export default TextWidgetContent;