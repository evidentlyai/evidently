import React, {FunctionComponent} from "react";
import {WidgetRenderer} from "../widgets/WidgetRenderer";
import {DashboardInfo} from "../api/Api";

export interface DashboardContentProps {
    info: DashboardInfo
}

export const DashboardContent : FunctionComponent<DashboardContentProps> = (props) =>
    <React.Fragment>{props.info.widgets.map(((wi, idx) => WidgetRenderer(`wi_${idx}`, wi)))}</React.Fragment>
