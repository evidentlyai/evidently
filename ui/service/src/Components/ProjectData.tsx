import * as React from 'react';
import {Box, Tab, Tabs, Link} from "@material-ui/core";
import {ReportViewer} from "./ReportViewer";
import {Link as RouterLink, useParams} from "react-router-dom";
import {Reports} from "./Reports";
import {TestSuites} from "./TestSuites";
import { ProjectDashboard } from '../lib/App';


interface TabPanelProps {
  children?: React.ReactNode;
  index: any;
  value: any;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

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
    let { projectId, page, reportId } = useParams();
    page = page ?? "";
    return <>
        <Tabs value={page} aria-label="simple tabs example">
            <Link component={RouterLink} to={`/projects/${projectId}`}><Tab label="Dashboard" {...a11yProps(0)} value={"dashboard"} /></Link>
            <Link component={RouterLink} to={`/projects/${projectId}/reports`}><Tab label="Reports" {...a11yProps(1)} value={"reports"} /></Link>
            <Link component={RouterLink} to={`/projects/${projectId}/test_suites`}><Tab label="Test Suites" {...a11yProps(2)} value={"test_suites"} /></Link>
            <Tab label="Comparisons" {...a11yProps(3)} disabled={true}/>
        </Tabs>
        <TabPanel value={page} index={""}>
            <ProjectDashboard projectId={projectId!} />
        </TabPanel>
        <TabPanel value={page} index={"reports"}>
            {reportId ? <ReportViewer projectId={projectId!} reportId={reportId} /> : <Reports projectId={projectId!}/> }
        </TabPanel>
        <TabPanel value={page} index={"test_suites"}>
            {reportId ? <ReportViewer projectId={projectId!} reportId={reportId} /> : <TestSuites projectId={projectId!}/> }
        </TabPanel>
    </>
}