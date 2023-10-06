import React from "react";
import {ProjectDetails} from "../lib/api/Api";

export const ProjectContext = React.createContext<ProjectDetails>({id: "--none--", project_name: "--none--"});
