import FilterNoneOutlinedIcon from "@material-ui/icons/FilterNoneOutlined";
import * as React from "react";
import {CSSProperties} from "react";

export const TextWithCopyIcon = (props: {showText: string, copyText: string, style?: CSSProperties}) => {
    return <>
        <div onClick={() => navigator.clipboard.writeText(props.copyText)}
             style={{...props.style, cursor: "pointer"}}
        >
            {props.showText}<FilterNoneOutlinedIcon
            style={{marginBottom: "-0.2rem", paddingLeft: "3px"}} fontSize={"small"}/>
        </div>
    </>
}