import React from 'react';
import ReactDOM from 'react-dom';
import {ProjectReport} from './lib/App';

import {AdditionalGraphInfo, DashboardInfo} from "./lib/api/Api";
import LocalApi from "./lib/api/LocalApi";
import {createTheme, ThemeProvider} from "@material-ui/core/styles";
import ApiContext from "./lib/contexts/ApiContext";



const theme = createTheme({
    shape: {
        borderRadius: 0
    },
    palette: {
        primary: {
            light: '#ed5455',
            main: '#ed0400',
            dark: '#d40400',
            contrastText: '#fff',
        },
        secondary: {
            light: '#61a0ff',
            main: '#3c7fdd',
            dark: '#61a0ff',
            contrastText: '#000',
        },
    },
    typography: {
        button: {
            fontWeight: "bold",
        },
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
    }
});


export function drawDashboard(dashboard: DashboardInfo, additionalGraphs: Map<string, AdditionalGraphInfo>, tagId: string) {
    ReactDOM.render(
        <React.StrictMode>
            <ThemeProvider theme={theme}>
                <ApiContext.Provider value={{Api: new LocalApi(dashboard, additionalGraphs)}}>
                    <ProjectReport projectId={"p1"} reportId={"d1"} />
                </ApiContext.Provider>
            </ThemeProvider>
        </React.StrictMode>,
        document.getElementById(tagId)
    );
}

// @ts-ignore
window.drawDashboard = drawDashboard;
