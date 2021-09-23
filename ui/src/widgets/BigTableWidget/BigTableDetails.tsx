import React from "react";

import Box from "@material-ui/core/Box";

import {BigTableRowDetails, WidgetSize} from "../../api/Api";

import DashboardContext from "../../contexts/DashboardContext";

import AutoTabs from "../../components/AutoTabs";
import LoadableView from "../../components/LoadableVIew";

import BigGraphWidgetContent from "../BigGraphWidgetContent";
import InsightBlock from "../InsightBlock";
import {WidgetRenderer} from "../WidgetRenderer";
import NotImplementedWidgetContent from "../NotImplementedWidgetContent";

interface BigTableDetailsProps {
    details: BigTableRowDetails;
    widgetSize: WidgetSize;
}

export const BigTableDetails: React.FunctionComponent<BigTableDetailsProps> = (props) => {
    return <DashboardContext.Consumer>{
        dashboardContext =>
            <Box>
                {props.details.parts.length > 1 ? <AutoTabs tabs={props.details.parts.map(part =>
                ({
                    title: part.title,
                    tab: (part.type ?? "graph") === "graph" ?
                        <LoadableView func={() => dashboardContext.getAdditionGraphData(part.id)}>
                            {params => <BigGraphWidgetContent {...params} widgetSize={props.widgetSize} />}
                        </LoadableView>
                        : (part.type ?? "graph") === "widget" ?
                        <LoadableView func={() => dashboardContext.getAdditionWidgetData(part.id)}>
                            {params => WidgetRenderer(part.id, params)}
                        </LoadableView>
                        : <NotImplementedWidgetContent />
                })
                )}/>
                : <LoadableView func={() => dashboardContext.getAdditionGraphData(props.details.parts[0].id)}>
                        {params => <BigGraphWidgetContent {...params} widgetSize={props.widgetSize} />}
                    </LoadableView>}
                {props.details.insights.map(row => <InsightBlock data={row} />)}
            </Box>
    }</DashboardContext.Consumer>;
}