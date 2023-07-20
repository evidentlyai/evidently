import React from "react";

import DashboardContext from "../../contexts/DashboardContext";
import LoadableView from "../../components/LoadableVIew";
import BigGraphWidgetContent from "../BigGraphWidgetContent";
import {WidgetSize} from "../../api/Api";

interface RowDetailsProps {
    graphId: string;
    widgetSize: WidgetSize;
}

export const GraphDetails: React.FunctionComponent<RowDetailsProps> = (props) => {
    return <DashboardContext.Consumer>{
        dashboardContext => <LoadableView func={() => dashboardContext.getAdditionGraphData(props.graphId)}>
            {params => <BigGraphWidgetContent {...params} widgetSize={props.widgetSize} />}
        </LoadableView>
    }</DashboardContext.Consumer>;
}