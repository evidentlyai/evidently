import React from "react";
import Box from "@material-ui/core/Box";

import {WithStyles, WithTheme} from "@material-ui/core/styles";
import {ResponsiveLineCanvas} from "@nivo/line";

import {BigTableDataRow, LineGraphOptions} from "../../api/Api";
import withTheme from "@material-ui/core/styles/withTheme";

interface LineGraphColumnProps extends LineGraphOptions {
    data: BigTableDataRow;
}

const _LineGraphColumn: React.FunctionComponent<LineGraphColumnProps & WithStyles & WithTheme> = (props) => {
    return <Box className={props.classes.graph}>
        <ResponsiveLineCanvas
            data={[{
                id: "1",
                data: props.data[props.xField].map((val: any, idx: number) => ({
                    x: val,
                    y: props.data[props.yField][idx]
                }))
            }]}
            margin={{top: 0, right: 0, bottom: 0, left: 0}}
            xScale={{type: 'linear', min: 0, max: 25}}
            axisTop={null}
            colors={[props.theme.palette.primary.main]}
            axisRight={null}
            enableGridX={false}
            enableGridY={false}
        />
    </Box>
}

export const LineGraphColumn = withTheme(_LineGraphColumn)