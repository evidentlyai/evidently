import React from 'react';
import {createStyles, createTheme, ThemeProvider} from '@material-ui/core/styles';

import {AdditionalGraphInfo, DashboardInfo} from "./api/Api";
import ApiContext from "./contexts/ApiContext";
import DashboardContext, {CreateDashboardContextState} from "./contexts/DashboardContext";
import SummaryView from "./components/SummaryView";
import LoadableView from "./components/LoadableVIew";
import LocalApi from "./api/LocalApi";
import {withStyles} from "@material-ui/core/styles";


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

const reset = createStyles({".reset-styles h5": {all: "initial"}})

function App(props: {dashboard: DashboardInfo, additionalGraphs: Map<string, AdditionalGraphInfo>}) {
    return (
        <div className={"reset-styles"}>
        <ThemeProvider theme={theme}>
            <ApiContext.Provider value={{Api: new LocalApi(props.dashboard, props.additionalGraphs)}}>
                <ApiContext.Consumer>
                    {api =>
                        <DashboardContext.Provider value={CreateDashboardContextState(
                            graphId => api.Api!.getAdditionalGraphData(
                                "",
                                "",
                                graphId
                            )
                        )}>
                            <LoadableView func={() => api.Api.getDashboard("", "")}>
                                {
                                    params => <SummaryView showHeader={false} dashboardInfo={params} />
                                }
                            </LoadableView>

                        </DashboardContext.Provider>
                    }
                </ApiContext.Consumer>
            </ApiContext.Provider>
        </ThemeProvider>
        </div>
    );
}

export default withStyles(reset)(App);
