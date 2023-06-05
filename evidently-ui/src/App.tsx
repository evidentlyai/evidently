import React from 'react';
import {createTheme, ThemeProvider} from '@material-ui/core/styles';

import {AdditionalGraphInfo, Api, DashboardInfo} from "./api/Api";
import ApiContext from "./contexts/ApiContext";
import DashboardContext, {CreateDashboardContextState} from "./contexts/DashboardContext";
import LoadableView from "./components/LoadableVIew";
import LocalApi from "./api/LocalApi";
import {DashboardContent} from "./components/DashboardContent";
import {Grid} from "@material-ui/core";


export const theme = createTheme({
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

export function Report(props: {}) {
    return <>
        <ApiContext.Consumer>
            {api =>
                <DashboardContext.Provider value={CreateDashboardContextState(
                    {
                        getAdditionGraphData: graphId => api.Api!.getAdditionalGraphData(
                            "p1",
                            "d1",
                            graphId
                        ),
                        getAdditionWidgetData: widgetId => api.Api!.getAdditionalWidgetData(
                            "p1",
                            "d1",
                            widgetId
                        ),
                    }
                )}>
                    <LoadableView func={() => api.Api.getDashboard("p1", "d1")}>
                        {
                            params => <Grid container spacing={3} direction="row" alignItems="stretch">
                                <DashboardContent info={params}/>
                            </Grid>
                        }
                    </LoadableView>

                </DashboardContext.Provider>
            }
        </ApiContext.Consumer>
    </>
}


export function App(props: { api: Api }) {
    return (
        <ThemeProvider theme={theme}>
            <ApiContext.Provider value={{Api: props.api}}>
                <Report />
            </ApiContext.Provider>
        </ThemeProvider>
    );
}
