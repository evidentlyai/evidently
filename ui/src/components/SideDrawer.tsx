import React from "react";

import Divider from "@material-ui/core/Divider";
import Drawer, {DrawerProps} from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import {makeStyles, Theme} from "@material-ui/core/styles";

import AddIcon from "@material-ui/icons/Add";
import LabelIcon from "@material-ui/icons/Label";
import ListIcon from "@material-ui/icons/List";
import PeopleIcon from '@material-ui/icons/People';
import SettingsIcon from '@material-ui/icons/Settings';

import ProjectsContext from "../contexts/ProjectsContext";

interface SideDrawerProps extends DrawerProps {
}

const styles = makeStyles((theme: Theme) => ({
    inner: {
        paddingLeft: theme.spacing(4)
    },
    inner2: {
        paddingLeft: theme.spacing(8)
    },
    inner3: {
        paddingLeft: theme.spacing(12)
    },
}))


const SideDrawer: React.FunctionComponent<SideDrawerProps> = (props) => {
    const classes = styles()
    return <ProjectsContext.Consumer>
        {projects => (
            <Drawer anchor={"left"} {...props} >
                <List dense>
                    <ListItem button key={"all_projects"}>
                        <ListItemIcon><ListIcon/></ListItemIcon>
                        <ListItemText primary={"All Projects"}/>
                    </ListItem>
                    <List dense>
                        {projects.Projects.map((pr, idx) => (
                            <ListItem button key={pr.id} className={classes.inner} onClick={() => {
                                projects.ChangeProject?.(pr.id);
                                props.onClose?.({}, "backdropClick");
                            }}>
                                <ListItemIcon><LabelIcon/></ListItemIcon>
                                <ListItemText primary={pr.title}/>
                            </ListItem>
                        ))}
                    </List>
                    <ListItem button disabled={true} key={"add_new"}>
                        <ListItemIcon><AddIcon/></ListItemIcon>
                        <ListItemText primary={"Add new..."}/>
                    </ListItem>
                </List>
                <Divider/>
                {projects.CurrentProjectId ? (
                    <List dense>
                        {projects.Projects.find(p => p.id === projects.CurrentProjectId)?.sections.map(
                            (si, idx) => (
                                <div>
                                    <ListItem button key={si.id} className={classes.inner}
                                              disabled={si.disabled}
                                              onClick={() => {
                                                  projects.ChangeSection?.(projects.CurrentProjectId!, [si.id]);
                                                  props.onClose?.({}, "backdropClick");
                                              }}
                                    >
                                        <ListItemIcon><LabelIcon/></ListItemIcon>
                                        <ListItemText primary={si.name}/>
                                    </ListItem>
                                    {si.sections
                                        ? <List dense>{si.sections.map((si2, idx) => (
                                            <ListItem button key={si2.id} disabled={si2.disabled}
                                                      className={classes.inner2}
                                                      onClick={() => {
                                                          projects.ChangeSection?.(projects.CurrentProjectId!, [si.id, si2.id]);
                                                          props.onClose?.({}, "backdropClick");
                                                      }}
                                            >
                                                <ListItemIcon><LabelIcon/></ListItemIcon>
                                                <ListItemText primary={si2.name}/>
                                            </ListItem>))}
                                        </List>
                                        : ""}
                                </div>
                            )
                        )}
                    </List>) : <div/>}
                {projects.CurrentProjectId ? <Divider/> : <div/>}
                <List dense>
                    <ListItem button key={'team'}>
                        <ListItemIcon><PeopleIcon/></ListItemIcon>
                        <ListItemText primary={"Team"}/>
                    </ListItem>
                    <ListItem button key={'settings'}>
                        <ListItemIcon><SettingsIcon/></ListItemIcon>
                        <ListItemText primary={"Settings"}/>
                    </ListItem>
                </List>
            </Drawer>)}
    </ProjectsContext.Consumer>
}

export default SideDrawer;