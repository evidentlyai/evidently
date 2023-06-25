import * as React from 'react';
import {Box, Tab, Tabs, Link, Grid} from "@material-ui/core";
import {ReportViewer} from "./ReportViewer";
import {Link as RouterLink, useParams} from "react-router-dom";
import {Reports} from "./Reports";
import {TestSuites, TestSuitesHeader} from "./TestSuites";
import {ProjectDashboard} from '../lib/App';
import {ReportsHeader} from './ReportsHeader';
import {TextWithCopyIcon} from "./TextWithCopyIcon";
import {ProjectContext} from "../Contexts/ProjectContext";


interface TabPanelProps {
    children?: React.ReactNode;
    index: any;
    value: any;
}

function TabPanel(props: TabPanelProps) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box p={3}>
                    {children}
                </Box>
            )}
        </div>
    );
}


function a11yProps(index: any) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

export function ProjectData() {
    let {projectId, page, reportId} = useParams();
    page = page ?? "";
    return <>
        <ProjectContext.Consumer>
                {project => (<>
                    <Grid container spacing={2} direction="row" justifyContent="flex-start" alignItems="flex-end">
                        <Grid item xs={12}>
                            <TextWithCopyIcon showText={`project id: ${project.id}`} copyText={project.id} style={{fontSize: "0.75rem", color: "#aaaaaa"}} />
                        </Grid>
                    </Grid>
                    <Tabs value={page} aria-label="simple tabs example">
                        <Link component={RouterLink} to={`/projects/${projectId}`}><Tab
                            label="Dashboard" {...a11yProps(0)}
                            value={"dashboard"}/></Link>
                        <Link component={RouterLink} to={`/projects/${projectId}/reports`}><Tab
                            label="Reports" {...a11yProps(1)} value={"reports"}/></Link>
                        <Link component={RouterLink} to={`/projects/${projectId}/test_suites`}><Tab
                            label="Test Suites" {...a11yProps(2)} value={"test_suites"}/></Link>
                        <Tab label="Comparisons" {...a11yProps(3)} disabled={true}/>
                    </Tabs>
                    <TabPanel value={page} index={""}>
                        <ProjectDashboard projectId={projectId!}/>
                    </TabPanel>
                    <TabPanel value={page} index={"reports"}>
                        <ReportsHeader projectId={projectId!} reportId={reportId}/>
                        {reportId ? <ReportViewer projectId={projectId!} reportId={reportId}/> :
                            <Reports projectId={projectId!}/>}
                    </TabPanel>
                    <TabPanel value={page} index={"test_suites"}>
                        <TestSuitesHeader projectId={projectId!} reportId={reportId}/>
                        {reportId ? <ReportViewer projectId={projectId!} reportId={reportId}/> :
                            <TestSuites projectId={projectId!}/>}
                    </TabPanel>
                </>)}
        </ProjectContext.Consumer>
    </>
}