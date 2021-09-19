import React from 'react';

import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

import ListIcon from "@material-ui/icons/List";

import ProjectsContext from "../contexts/ProjectsContext";

import TabbedLayout from "./TabbedLayout";

function ProjectList() {
    return (<TabbedLayout path={["Projects"]} tabs={[
            {
                icon: <ListIcon/>,
                title: "Projects",
                tab: <ProjectsContext.Consumer>
                    {projects =>
                        <List component="nav">
                                {projects.Projects.map(item =>
                                    <ListItem button onClick={() => projects.ChangeProject?.(item.id)}>
                                        <ListItemText primary={item.title}/>
                                    </ListItem>)}
                            </List>}
                </ProjectsContext.Consumer>
            }
        ]
        }>
        </TabbedLayout>
    );
}

export default ProjectList;
