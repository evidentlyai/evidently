import React, {ReactNode} from "react";

import Box from "@material-ui/core/Box"
import Tab from "@material-ui/core/Tab"
import Tabs from "@material-ui/core/Tabs"
import {createStyles, Theme, withStyles, WithStyles} from "@material-ui/core/styles"

export interface TabInfo {
    title: string;
    tab: ReactNode;
    link?: string;
    disabled?: boolean;
    icon?: ReactNode;
}

interface BaseTabsProps {
    activeTab: number;
    tabs: TabInfo[];
    tabStyle?: string;
    onNewTabSelected: (event: React.ChangeEvent<{}>, newTabIdx: number) => void;
}

const styles = (theme: Theme) => createStyles({
    iconTab: {
        display: "flex",
    },
    activeTab: {
        backgroundColor: theme.palette.grey["100"]
    },
    background: {
        backgroundColor: theme.palette.grey["100"],
        padding: theme.spacing(1),
    },
    tab: {}
});

const BaseTabs: React.FunctionComponent<BaseTabsProps & WithStyles> = (props) => {
    const activeTab = props.activeTab === -1 ? 0 : props.activeTab;
    return <div>
        <Tabs value={activeTab}
              onChange={props.onNewTabSelected}
              indicatorColor="primary"
              textColor="primary"
        >
            {props.tabs.map((ti, idx) => (
                <Tab
                    // className={idx === activeTab ? props.classes.activeTab : props.classes.tab}
                    disabled={ti.disabled ?? false}
                    key={idx}
                    label={<div className={props.tabStyle}>
                        <div className={props.classes.iconTab}><span>{ti.icon}</span>{ti.title}</div>
                    </div>}
                />
            ))}
        </Tabs>
        <Box
            // className={props.classes.background}
        >
            {props.tabs.map((ti, idx) => (
                <div key={idx}
                     hidden={(props.activeTab === -1 ? 0 : props.activeTab) !== idx}>
                    {(props.activeTab === -1 ? 0 : props.activeTab) !== idx ? <div/> : ti.tab}
                </div>))}
        </Box>
    </div>
}

export default withStyles(styles)(BaseTabs);