import React from "react";

import Box from "@material-ui/core/Box";

import {WithStyles, WithTheme} from "@material-ui/core/styles";

import {ResponsiveScatterPlot} from "@nivo/scatterplot";

import {BigTableDataRow, LineGraphOptions} from "../../api/Api";
import withTheme from "@material-ui/core/styles/withTheme";

interface ScatterGraphColumnProps extends LineGraphOptions {
    data: BigTableDataRow;
}

const _ScatterGraphColumn: React.FunctionComponent<ScatterGraphColumnProps & WithStyles & WithTheme> = (props) => {
    return <Box className={props.classes.graph}>
        <ResponsiveScatterPlot
            data={[{
                id: "1",
                data: props.data[props.xField].map((val: any, idx: number) => ({
                    x: val,
                    y: props.data[props.yField][idx]
                }))
            }]}
            margin={{top: 3, right: 3, bottom: 3, left: 3}}
            xScale={{type: 'linear', min: 0, max: 1000}}
            nodeSize={4}
            colors={[props.theme.palette.primary.main]}
            useMesh={false}
            axisTop={null}
            axisRight={null}
            enableGridX={false}
            enableGridY={false}
        />
    </Box>
}

export const ScatterGraphColumn = withTheme(_ScatterGraphColumn)