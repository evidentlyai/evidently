import React from "react";
import Box from "@material-ui/core/Box";

import {WithStyles, WithTheme} from "@material-ui/core/styles";

import {ResponsiveBarCanvas} from "@nivo/bar";

import {BigTableDataRow, LineGraphOptions} from "../../api/Api";
import withTheme from "@material-ui/core/styles/withTheme";

interface HistogramGraphColumnProps extends LineGraphOptions {
    data: BigTableDataRow;
}

const _HistogramGraphColumn: React.FunctionComponent<HistogramGraphColumnProps & WithStyles & WithTheme> = (props) => {
    return <Box className={props.classes.graph}>
        <ResponsiveBarCanvas
            data={props.data[props.xField].map((v: any, idx: number) => ({id: v, x: props.data[props.yField][idx]}))}
            margin={{top: 3, right: 3, bottom: 3, left: 3}}
            indexBy={"id"}
            keys={["x"]}
            colors={[props.theme.palette.primary.main]}
            axisTop={null}
            axisRight={null}
            enableGridX={false}
            enableGridY={false}
        />
    </Box>
}

export const HistogramGraphColumn = withTheme(_HistogramGraphColumn)