import React, {ReactNode, useState} from "react";

import Box from "@material-ui/core/Box";
import Popover from "@material-ui/core/Popover";
import Typography from "@material-ui/core/Typography";

import {createStyles, Theme, withStyles, WithStyles} from "@material-ui/core/styles";

import WarningIcon from "@material-ui/icons/Warning";

import MaterialTable, {Column, Options} from "material-table";

import {
    BigTableDataRow,
    BigTableWidgetParams,
    ColumnDefinition,
    HistogramGraphOptions,
    LineGraphOptions,
    ScatterGraphOptions,
    WidgetSize
} from "../../api/Api";

import {GraphDetails} from "./GraphDetails";
import {LineGraphColumn} from "./LineGraphColumn";
import {ScatterGraphColumn} from "./ScatterGraphColumn";
import {HistogramGraphColumn} from "./HistogramGraphColumn";
import {BigTableDetails} from "./BigTableDetails";

interface BigTableWidgetProps extends BigTableWidgetParams {
    widgetSize: WidgetSize;
}

const useStyles = (theme: Theme) => createStyles({
    graph: {
        maxWidth: 200,
        height: 50,
    },
    alert: {
        width: 50,
    },
    popup: {
        padding: theme.spacing(1),
    }
})

const GraphMapping =
    new Map<string, (def: ColumnDefinition, row: BigTableDataRow, classes: any) => React.ReactNode>([
        ["line", (def, row, classes) => row[def.field]
            ? <LineGraphColumn xField={(def.options as LineGraphOptions).xField}
                               yField={(def.options as LineGraphOptions).yField}
                               data={row[def.field]} classes={classes}/>
            : <div/>],
        ["scatter", (def, row, classes) => row[def.field]
            ? <ScatterGraphColumn xField={(def.options as ScatterGraphOptions).xField}
                                  yField={(def.options as ScatterGraphOptions).yField}
                                  data={row[def.field]} classes={classes}/>
            : <div/>],
        ["histogram", (def, row, classes) => row[def.field]
            ? <HistogramGraphColumn xField={(def.options as HistogramGraphOptions).xField}
                                    yField={(def.options as HistogramGraphOptions).yField}
                                    data={row[def.field]} classes={classes}/>
            : <div/>]
    ])

const GenerateColumns = <RowData extends object, >(columns: ColumnDefinition[], classes: any): Column<RowData>[] =>
    columns.map(def => ({def: def, gen: GraphMapping.get(def.type ?? "string")}))
        .map(({def, gen}) => gen
            ? ({...def, type: undefined, render: (row: BigTableDataRow) => gen(def, row, classes)})
            : ({...def, sorting: true, defaultSort: def.sort, type: "string"} as Column<RowData>))


interface InsightAlertProps {
    containerClass: string;
    popupClass: string;
    longText: ReactNode;
}


type InsightAlertState = { open: boolean, anchorEl?: EventTarget & HTMLElement };
const InsightAlert: React.FunctionComponent<InsightAlertProps> = (props) => {
    const [state, setState] = useState<InsightAlertState>({open: false, anchorEl: undefined})
    return <Box className={props.containerClass}
                onClick={(event) => setState(s => ({open: !s.open, anchorEl: event.currentTarget}))}
    ><WarningIcon/>
        <Popover open={state.open}
                 anchorEl={state.anchorEl}
                 anchorOrigin={{horizontal: "left", vertical: "bottom"}}
        ><Typography className={props.popupClass}>{props.longText}</Typography></Popover>
    </Box>
}

const BigTableWidgetContent: React.FunctionComponent<BigTableWidgetProps & WithStyles> = (props) => {
    const {columns, data} = props;
    const options = {search: true, showTitle: false, minBodyHeight: "10vh", pageSize: props.rowsPerPage ?? 5} as Options<any>;
    return <React.Fragment>
        <MaterialTable
            columns={(props.showInfoColumn ?? false)
                ? [...GenerateColumns(columns, props.classes),
                    {
                        title: "Info",
                        render: row => (<React.Fragment>{
                            row.details?.insights
                                ? <InsightAlert
                                    containerClass={props.classes.alert}
                                    popupClass={props.classes.popup}
                                    longText={`${row.details?.insights[0].title}: ${row.details?.insights[0].text}`}/>
                                : <div/>
                        }</React.Fragment>),
                        width: 50,
                    }]
                : [...GenerateColumns(columns, props.classes)]}
            data={data}

            detailPanel={rowData => (rowData.graphId
                ? <GraphDetails graphId={rowData.graphId} widgetSize={props.widgetSize}/>
                : rowData.details
                    ? <BigTableDetails details={rowData.details} widgetSize={props.widgetSize}/>
                    : null)}
            options={options}
        />
    </React.Fragment>
}

export default withStyles(useStyles)(BigTableWidgetContent);