import React from "react";

import Grid from "@material-ui/core/Grid";

import {createStyles, Theme, WithStyles, withStyles} from "@material-ui/core";

const useStyles = (theme: Theme) => createStyles({
    base: {
        marginTop: theme.spacing(1),
    }
});

interface WidgetPanelProps {
}

class WidgetPanel extends React.Component<WidgetPanelProps & WithStyles, {}> {
    render() {
        return <Grid container
                     alignItems={"stretch"}
                     spacing={1}
                     direction={"row"}
                     className={this.props.classes.base}>
                {this.props.children}
        </Grid>;
    }
}

export default withStyles(useStyles)(WidgetPanel);