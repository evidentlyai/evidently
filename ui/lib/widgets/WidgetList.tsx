import React from "react";
import {WidgetListParams} from "../api/Api";
import WidgetPanel from "./WidgetPanel";
import {WidgetRenderer} from "./WidgetRenderer";
import {Grid} from "@material-ui/core";
import Button from "@material-ui/core/Button";

import ArrowLeft from "@material-ui/icons/ArrowLeft";
import ArrowRight from "@material-ui/icons/ArrowRight";


const WidgetList: React.FunctionComponent<WidgetListParams & { widgetSize: number }> = (params) => {
    let [pageState, setPageState] = React.useState({page: 0})
    let drawWidgets = params.widgets.slice(pageState.page * params.pageSize, (pageState.page + 1) * params.pageSize);
    return <WidgetPanel>
        {drawWidgets.map((wi, idx) => WidgetRenderer(`wi_${idx}`, wi))}
        <Grid item xs={12}>
            <Button startIcon={<ArrowLeft />}
                    disabled={pageState.page === 0}
                    onClick={() => setPageState(prev => ({page: prev.page - 1}))}>Previous</Button>
            <span>{pageState.page + 1} / {Math.round(params.widgets.length / params.pageSize)}</span>
            <Button endIcon={<ArrowRight />}
                    disabled={pageState.page >= (params.widgets.length / params.pageSize - 1)}
                    onClick={() => setPageState(prev => ({page: prev.page + 1}))}>Next</Button>
        </Grid>
    </WidgetPanel>;
}


export default WidgetList;