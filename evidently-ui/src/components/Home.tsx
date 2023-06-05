import React from 'react';

import Paper from "@material-ui/core/Paper";
import {makeStyles} from "@material-ui/core/styles";

import {ProjectInfo, SectionInfo} from "../api/Api";
import ApiContext from "../contexts/ApiContext";
import ProjectsContext, {ProjectsContextState} from "../contexts/ProjectsContext";

import SummaryView from "./SummaryView";
import LoadableView from "./LoadableVIew";
import BaseLayout from "./BaseLayout";
import BaseTabs, {TabInfo} from "./BaseTabs";
import Grid from "@material-ui/core/Grid";

interface HomeProps {
    projectId: string;
    project: ProjectInfo;
    dashboard: string[];
}

const useStyles = makeStyles((theme) => ({
    base: {
        backgroundColor: theme.palette.grey["200"],
        padding: 10,
    },
    tabFirst: {},
    tabSecond: {
        fontSize: "smaller"
    }
}));

function ExpandSection(projects: ProjectsContextState, projectId: string, leftDepth: string[], prevSections: string[], section: SectionInfo, tabClass: string): TabInfo {
    if (section.sections) {
        return {
            title: section.name,
            disabled: section.disabled,
            tab: <BaseTabs
                activeTab={section.sections.findIndex(t => t.id === leftDepth[0])}
                tabStyle={tabClass}
                tabs={
                    section.sections
                        .map(s => ExpandSection(
                            projects,
                            projectId,
                            [...leftDepth.slice(1)],
                            [...prevSections, section.id],
                            s,
                            tabClass))}
                onNewTabSelected={(event, newTabIdx) =>
                    projects.ChangeSection?.(projectId, [...prevSections, section.id, section.sections![newTabIdx].id])}
            />
        }
    } else {
        return {
            title: section.name,
            disabled: section.disabled,
            tab: !section.disabled ? <ApiContext.Consumer>
                {(api) => <LoadableView
                    func={() => api.Api.getDashboard(projectId, [...prevSections, section.id].join("."))}>
                    {val => (<SummaryView dashboardInfo={val}/>)}
                </LoadableView>
                }
            </ApiContext.Consumer> : <div/>
        }
    }
}

const Home: React.FunctionComponent<HomeProps> = (props) => {
    const classes = useStyles();
    return (
        <BaseLayout path={["Projects", props.project.title]}>
            <Paper elevation={0} className={classes.base}>
                <ProjectsContext.Consumer>
                    {projects =>
                        (<BaseTabs
                            tabStyle={classes.tabFirst}
                            tabs={
                                props.project
                                    .sections
                                    .map(s => ExpandSection(
                                        projects,
                                        props.projectId,
                                        [...props.dashboard.slice(1)],
                                        [],
                                        s,
                                        classes.tabSecond
                                    ))
                            }
                            activeTab={props.project.sections.findIndex(t => t.id === props.dashboard[0])}
                            onNewTabSelected={(event, newTabIdx) =>
                                projects.ChangeSection?.(props.projectId, [props.project.sections[newTabIdx].id])}
                            // tabClicked={tab => tab.link!}
                        />)}
                </ProjectsContext.Consumer>
            </Paper>
        </BaseLayout>
    );
}

export default Home;
