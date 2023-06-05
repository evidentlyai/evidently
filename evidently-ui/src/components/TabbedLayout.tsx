import React, {ReactNode, useState} from "react";

import Box from "@material-ui/core/Box";
import Paper from "@material-ui/core/Paper";
import Tab from "@material-ui/core/Tab";
import Tabs from "@material-ui/core/Tabs";

import {makeStyles} from "@material-ui/core/styles";

import BaseLayout, {BaseLayoutProps} from "./BaseLayout";

interface TabbedLayoutState {
    activeTab: number;
}

interface TabInfo {
    title: string;
    tab: ReactNode;
    disabled?: boolean;
    icon?: ReactNode;
}

interface TabbedLayoutProps extends BaseLayoutProps {
    tabs: TabInfo[];
}

const useStyles = makeStyles((theme) => ({
    base: {
        marginTop: 5,
        backgroundColor: theme.palette.grey['100'],
        padding: 10,
    },
    iconTab: {
        display: "flex",
    }
}));


const TabbedLayout: React.FunctionComponent<TabbedLayoutProps> = (props) => {
    let [state, setState] = useState<TabbedLayoutState>(() => ({activeTab: 0}));
    let classes = useStyles();
    return (
        <BaseLayout {...props}>
            <Paper elevation={0} className={classes.base}>
                <Tabs value={state.activeTab} aria-label="simple tabs example" onChange={
                    (_, newTab) => setState(s => ({...s, activeTab: newTab}))
                }>
                    {props.tabs.map((ti, idx) => (
                        <Tab disabled={ti.disabled ?? false} key={idx} label={
                            <div className={classes.iconTab}><span>{ti.icon}</span>{ti.title}</div>}/>))}
                </Tabs>
                <Box>
                    {props.tabs.map((ti, idx) => (<div key={idx} hidden={state.activeTab !== idx}>{ti.tab}</div>))}
                </Box>
            </Paper>
        </BaseLayout>
    )
}

export default TabbedLayout;