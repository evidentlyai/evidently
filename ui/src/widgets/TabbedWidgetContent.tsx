import React from "react";

import {MultiTabWidgetParams} from "../api/Api";

import AutoTabs from "../components/AutoTabs";
import {WidgetRenderer} from "./WidgetRenderer";

const TabbedWidgetContent: React.FunctionComponent<MultiTabWidgetParams & {id: string, widgetSize: number}> =
    (props) => {
    console.log(props)
        return (<AutoTabs
            tabs={props.tabs.map((g, idx) => ({
                title: g.title,
                tab: WidgetRenderer(props.id + "1", g.widget),
            }))}
        />)
    }

export default TabbedWidgetContent;