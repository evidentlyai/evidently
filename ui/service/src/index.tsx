import ReactDOM from 'react-dom';
import './index.css';

import {createTheme, ThemeProvider} from "@material-ui/core/styles";
import reportWebVitals from './reportWebVitals';
// import LocalApi from "./lib/api/LocalApi";
import RemoteApi from "./api/RemoteApi";
import ApiContext from "./lib/contexts/ApiContext";
import {
    createBrowserRouter, Outlet,
    RouterProvider, useParams,
} from "react-router-dom";
import "./index.css";
import {ServiceMainPage} from "./Components/ServiceMainPage";
import {ProjectData} from "./Components/ProjectData";
import {ProjectList, action as projectListAction, loader as projectListLoader } from "./Components/ProjectList";
import {ServiceHeader} from "./Components/ServiceHeader";
import { Typography } from '@material-ui/core';
import { NavigationProgress } from './Components/NavigationProgress';


const api = new RemoteApi("/api");


const HomePage = () => {
    let {projectId, dashboardId} = useParams();
    return <ThemeProvider theme={theme}>
        <ApiContext.Provider value={{Api: api}}>
            <ServiceHeader api={api}/>
            <NavigationProgress />
            <ServiceMainPage projectId={projectId} reportId={dashboardId}>
                <Outlet />
            </ServiceMainPage>
        </ApiContext.Provider>
    </ThemeProvider>
}


const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />,
        children: [
            {
                index: true,
                element: <ProjectList />,
                loader: projectListLoader,
                action: projectListAction,
                errorElement: <Typography variant='h4'> Something went wrong...</Typography>,
            },
            {
                path: "projects/:projectId",
                element: <ProjectData />,
            },
            {
                path: "projects/:projectId/:page",
                element: <ProjectData />,
            },
            {
                path: "projects/:projectId/:page/:reportId",
                element: <ProjectData />,
            }
        ]
    },
]);
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

// const localApi = new LocalApi({
//     "name": "Report",
//     "widgets": [
//         {
//         "type": "counter",
//         "title": "",
//         "size": 2,
//         "id": "69e09b1f-9576-4eb3-8ba9-ff1d9ed09a90",
//         "details": "",
//         "alertsPosition": null,
//         "alertStats": null,
//         "params": {
//             "counters": [{
//                 "value": "Dataset Drift",
//                 "label": "Dataset Drift is NOT detected. Dataset drift detection threshold is 0.5"
//             }]
//         },
//         "insights": [],
//         "alerts": [],
//         "tabs": [],
//         "widgets": [],
//         "pageSize": 5
//     }
//     ,
//         {
//         "type": "counter",
//         "title": "",
//         "size": 2,
//         "id": "3bf77e34-b4e8-491d-99b5-7e7ecd8c44ed",
//         "details": "",
//         "alertsPosition": null,
//         "alertStats": null,
//         "params": {
//             "counters": [{"value": "15", "label": "Columns"}, {
//                 "value": "6",
//                 "label": "Drifted Columns"
//             }, {"value": "0.4", "label": "Share of Drifted Columns"}]
//         },
//         "insights": [],
//         "alerts": [],
//         "tabs": [],
//         "widgets": [],
//         "pageSize": 5
//     }
//     , {
//         "type": "counter",
//         "title": "",
//         "size": 2,
//         "id": "75adc7d2-38ac-481c-b069-e932d908742c",
//         "details": "",
//         "alertsPosition": null,
//         "alertStats": null,
//         "params": {"counters": [{"value": "", "label": "Data Drift Summary"}]},
//         "insights": [],
//         "alerts": [],
//         "tabs": [],
//         "widgets": [],
//         "pageSize": 5
//     },
//         {
//         "type": "big_table",
//         "title": "Drift is detected for 40.0% of columns (6 out of 15).",
//         "size": 2,
//         "id": "3614c803-23ef-4a5d-9b23-5bd5b587e4d0",
//         "details": "",
//         "alertsPosition": "row",
//         "alertStats": null,
//         "params": {
//             "rowsPerPage": 10,
//             "columns": [{"title": "Column", "field": "column_name"}, {
//                 "title": "Type",
//                 "field": "column_type"
//             }, {
//                 "title": "Reference Distribution",
//                 "field": "reference_distribution",
//                 "type": "histogram",
//                 "options": {"xField": "x", "yField": "y", "color": "#ed0400"}
//             }, {
//                 "title": "Current Distribution",
//                 "field": "current_distribution",
//                 "type": "histogram",
//                 "options": {"xField": "x", "yField": "y", "color": "#ed0400"}
//             }, {"title": "Data Drift", "field": "data_drift"}, {
//                 "title": "Stat Test",
//                 "field": "stattest_name"
//             }, {"title": "Drift Score", "field": "drift_score"}],
//             "data": [{
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "b42d9c86-f7c4-440d-984e-7bfefd952368",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "education",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["10th", "11th", "12th", "1st-4th", "5th-6th", "7th-8th", "9th", "Assoc-acdm", "Assoc-voc", "Bachelors", "Doctorate", "HS-grad", "Masters", "Preschool", "Prof-school", "Some-college"],
//                     "y": [1389, 1812, 657, 247, 509, 955, 756, 1601, 2061, 0, 594, 0, 2657, 83, 834, 0]
//                 },
//                 "current_distribution": {
//                     "x": ["10th", "11th", "12th", "1st-4th", "5th-6th", "7th-8th", "9th", "Assoc-acdm", "Assoc-voc", "Bachelors", "Doctorate", "HS-grad", "Masters", "Preschool", "Prof-school", "Some-college"],
//                     "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 7535, 0, 14892, 0, 0, 0, 10260]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 15.016729
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "c19dbddb-91cd-4a6c-9d51-3ca3d77185b4",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "bcb4422e-911c-4078-ad33-9f99835c29d2", "type": "widget"}]
//                 },
//                 "column_name": "capital-loss",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [0.0, 390.0, 780.0, 1170.0, 1560.0, 1950.0, 2340.0, 2730.0, 3120.0, 3510.0, 3900.0],
//                     "y": [0.002434221847856606, 1.0868679183762194e-06, 1.2680125714389225e-06, 7.970364734758943e-06, 6.23137606535699e-05, 3.967067902073201e-05, 1.4672716898078962e-05, 2.173735836752439e-06, 1.811446530627032e-07, 5.434339591881097e-07]
//                 },
//                 "current_distribution": {
//                     "x": [0.0, 435.6, 871.2, 1306.8000000000002, 1742.4, 2178.0, 2613.6000000000004, 3049.2000000000003, 3484.8, 3920.4, 4356.0],
//                     "y": [0.0021929683487458603, 1.1912910903101098e-06, 1.257473928660671e-06, 3.4745990134044877e-05, 5.201971094354147e-05, 1.2310007933204457e-05, 5.95645545155055e-07, 6.618283835056166e-08, 3.309141917528083e-07, 1.98548515051685e-07]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.346362
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "bc950d76-1724-44cd-948b-a02ccb3366b6",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "occupation",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Adm-clerical", "Armed-Forces", "Craft-repair", "Exec-managerial", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Other-service", "Priv-house-serv", "Prof-specialty", "Protective-serv", "Sales", "Tech-support", "Transport-moving"],
//                     "y": [941, 5, 1611, 1581, 551, 650, 900, 1557, 113, 2956, 202, 1153, 404, 629]
//                 },
//                 "current_distribution": {
//                     "x": ["Adm-clerical", "Armed-Forces", "Craft-repair", "Exec-managerial", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Other-service", "Priv-house-serv", "Prof-specialty", "Protective-serv", "Sales", "Tech-support", "Transport-moving"],
//                     "y": [4670, 10, 4501, 4505, 939, 1422, 2122, 3366, 129, 3216, 781, 4351, 1042, 1726]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.191829
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "444d1430-55e2-45fa-b488-857209bc1d85",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "native-country",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Cambodia", "Canada", "China", "Columbia", "Cuba", "Dominican-Republic", "Ecuador", "El-Salvador", "England", "France", "Germany", "Greece", "Guatemala", "Haiti", "Holand-Netherlands", "Honduras", "Hong", "Hungary", "India", "Iran", "Ireland", "Italy", "Jamaica", "Japan", "Laos", "Mexico", "Nicaragua", "Outlying-US(Guam-USVI-etc)", "Peru", "Philippines", "Poland", "Portugal", "Puerto-Rico", "Scotland", "South", "Taiwan", "Thailand", "Trinadad&Tobago", "United-States", "Vietnam", "Yugoslavia"],
//                     "y": [6, 59, 56, 34, 64, 58, 15, 95, 41, 16, 59, 19, 59, 29, 0, 8, 16, 6, 88, 22, 9, 49, 31, 24, 10, 639, 18, 5, 12, 79, 30, 40, 68, 5, 24, 32, 11, 11, 11984, 23, 7]
//                 },
//                 "current_distribution": {
//                     "x": ["Cambodia", "Canada", "China", "Columbia", "Cuba", "Dominican-Republic", "Ecuador", "El-Salvador", "England", "France", "Germany", "Greece", "Guatemala", "Haiti", "Holand-Netherlands", "Honduras", "Hong", "Hungary", "India", "Iran", "Ireland", "Italy", "Jamaica", "Japan", "Laos", "Mexico", "Nicaragua", "Outlying-US(Guam-USVI-etc)", "Peru", "Philippines", "Poland", "Portugal", "Puerto-Rico", "Scotland", "South", "Taiwan", "Thailand", "Trinadad&Tobago", "United-States", "Vietnam", "Yugoslavia"],
//                     "y": [22, 123, 66, 51, 74, 45, 30, 60, 86, 22, 147, 30, 29, 46, 1, 12, 14, 13, 63, 37, 28, 56, 75, 68, 13, 312, 31, 18, 34, 216, 57, 27, 116, 16, 91, 33, 19, 16, 31848, 63, 16]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.099832
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "dc408668-9357-4cfb-8a0b-64e27e770cf8",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "ab655869-898b-4ea4-b7c9-78f826d80529", "type": "widget"}]
//                 },
//                 "column_name": "fnlwgt",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [13769.0, 157935.6, 302102.2, 446268.80000000005, 590435.4, 734602.0, 878768.6000000001, 1022935.2000000001, 1167101.8, 1311268.4000000001, 1455435.0],
//                     "y": [2.7559464969112866e-06, 3.229318530342351e-06, 8.061045496833332e-07, 1.1172756068559274e-07, 2.1561459079675788e-08, 8.330563735329276e-09, 9.80066321803445e-10, 9.80066321803445e-10, 4.900331609017221e-10, 9.80066321803446e-10]
//                 },
//                 "current_distribution": {
//                     "x": [12285.0, 160096.5, 307908.0, 455719.5, 603531.0, 751342.5, 899154.0, 1046965.5, 1194777.0, 1342588.5, 1490400.0],
//                     "y": [2.7682113067215177e-06, 3.1635586130503076e-06, 7.115081270288237e-07, 9.166908434856009e-08, 2.184454775965687e-08, 4.2908933099325996e-09, 2.340487259963236e-09, 1.170243629981618e-09, 3.900812099938727e-10, 3.900812099938727e-10]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 0.027831
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "d0d49b11-4751-421e-ac1c-c2fcb7ddbb76",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "workclass",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Federal-gov", "Local-gov", "Never-worked", "Private", "Self-emp-inc", "Self-emp-not-inc", "State-gov", "Without-pay"],
//                     "y": [361, 1086, 6, 9386, 519, 1252, 645, 4]
//                 },
//                 "current_distribution": {
//                     "x": ["Federal-gov", "Local-gov", "Never-worked", "Private", "Self-emp-inc", "Self-emp-not-inc", "State-gov", "Without-pay"],
//                     "y": [1071, 2050, 4, 24520, 1176, 2610, 1336, 17]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.013186
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "0ce050d7-2786-4edb-9ddb-04e48ff6573e",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "marital-status",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Divorced", "Married-AF-spouse", "Married-civ-spouse", "Married-spouse-absent", "Never-married", "Separated", "Widowed"],
//                     "y": [1814, 7, 6821, 222, 4312, 470, 509]
//                 },
//                 "current_distribution": {
//                     "x": ["Divorced", "Married-AF-spouse", "Married-civ-spouse", "Married-spouse-absent", "Never-married", "Separated", "Widowed"],
//                     "y": [4819, 30, 15558, 406, 11805, 1060, 1009]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.010267
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "a123584f-e440-4563-bdc6-5d59311ead72",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "class",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {"x": ["<=50K", ">50K"], "y": [10347, 3808]},
//                 "current_distribution": {"x": ["<=50K", ">50K"], "y": [26808, 7879]},
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.009418
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "cf44cf07-89b1-4b1b-be4b-0edb9f262011",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "relationship",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Husband", "Not-in-family", "Other-relative", "Own-child", "Unmarried", "Wife"],
//                     "y": [6034, 3510, 468, 1947, 1521, 675]
//                 },
//                 "current_distribution": {
//                     "x": ["Husband", "Not-in-family", "Other-relative", "Own-child", "Unmarried", "Wife"],
//                     "y": [13682, 9073, 1038, 5634, 3604, 1656]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.007765
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "70b9d89a-533c-44c6-b70f-86eb0a7aea6b",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "race",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {
//                     "x": ["Amer-Indian-Eskimo", "Asian-Pac-Islander", "Black", "Other", "White"],
//                     "y": [141, 473, 1323, 166, 12052]
//                 },
//                 "current_distribution": {
//                     "x": ["Amer-Indian-Eskimo", "Asian-Pac-Islander", "Black", "Other", "White"],
//                     "y": [329, 1046, 3362, 240, 29710]
//                 },
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.003051
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DISTRIBUTION",
//                         "id": "79b78caf-2afa-4b00-89f1-35293b537e06",
//                         "type": "widget"
//                     }]
//                 },
//                 "column_name": "sex",
//                 "column_type": "cat",
//                 "stattest_name": "PSI",
//                 "reference_distribution": {"x": ["Female", "Male"], "y": [4440, 9715]},
//                 "current_distribution": {"x": ["Female", "Male"], "y": [11752, 22935]},
//                 "data_drift": "Not Detected",
//                 "drift_score": 0.002874
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "1aaf8116-ced3-4ea4-a0ac-dcfb62a79c27",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "7f97422a-386b-4fcf-96da-604a99df4094", "type": "widget"}]
//                 },
//                 "column_name": "capital-gain",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [0.0, 9999.9, 19999.8, 29999.699999999997, 39999.6, 49999.5, 59999.399999999994, 69999.3, 79999.2, 89999.09999999999, 99999.0],
//                     "y": [9.634147913361861e-05, 2.2395137409516095e-06, 4.804004239265283e-07, 1.4129424233133181e-08, 1.4129424233133181e-08, 0.0, 0.0, 0.0, 0.0, 9.113478630370894e-07]
//                 },
//                 "current_distribution": {
//                     "x": [0.0, 9999.9, 19999.8, 29999.699999999997, 39999.6, 49999.5, 59999.399999999994, 69999.3, 79999.2, 89999.09999999999, 99999.0],
//                     "y": [9.822510079686088e-05, 1.2569676248842519e-06, 1.7297719608498882e-07, 1.1531813072332584e-08, 2.882953268083146e-09, 0.0, 0.0, 0.0, 0.0, 3.3153962582956155e-07]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 0.000165
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "f1fd8224-6b26-4776-8815-8629da316488",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "3efbf925-51c1-4d37-99f9-7725b2805fee", "type": "widget"}]
//                 },
//                 "column_name": "hours-per-week",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [1.0, 10.8, 20.6, 30.400000000000002, 40.2, 50.0, 59.800000000000004, 69.60000000000001, 79.4, 89.2, 99.0],
//                     "y": [0.003070956393860971, 0.008196425868121887, 0.007028597380315601, 0.05289830520692911, 0.009313792631146421, 0.012579387106308432, 0.005968901159898786, 0.001585939921712239, 0.0007785523252041899, 0.0006199583330329661]
//                 },
//                 "current_distribution": {
//                     "x": [1.0, 10.8, 20.6, 30.400000000000002, 40.2, 50.0, 59.800000000000004, 69.60000000000001, 79.4, 89.2, 99.0],
//                     "y": [0.0020562899821905873, 0.006445395351902112, 0.007127883586334467, 0.0567789026412883, 0.009940205793736761, 0.012011204574083209, 0.005336351970949533, 0.0013620347092335367, 0.0006089442436530068, 0.0003736034731590911]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 0.0
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "f6075e21-a461-4c44-b653-274e97e4de91",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "d9a68338-162c-426c-b40b-bdc2937eceef", "type": "widget"}]
//                 },
//                 "column_name": "age",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [17.0, 24.3, 31.6, 38.9, 46.2, 53.5, 60.8, 68.1, 75.4, 82.7, 90.0],
//                     "y": [0.02104876054252575, 0.020739077628796638, 0.02384558435714183, 0.026835959992838568, 0.018658395552179158, 0.012580868370245284, 0.00869047676652328, 0.0029516652714806184, 0.001287119610186633, 0.000348393277945254]
//                 },
//                 "current_distribution": {
//                     "x": [17.0, 24.3, 31.6, 38.9, 46.2, 53.5, 60.8, 68.1, 75.4, 82.7, 90.0],
//                     "y": [0.02471021672878118, 0.025839691234843417, 0.0262859521410848, 0.025211766596857754, 0.015942967066340047, 0.010173168977679455, 0.0061528716099474344, 0.0018640278561586543, 0.000568686464590777, 0.0002369526935794904]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 0.0
//             }, {
//                 "details": {
//                     "parts": [{
//                         "title": "DATA DRIFT",
//                         "id": "4f508dc8-94d4-485f-ac50-903490f3cf52",
//                         "type": "widget"
//                     }, {"title": "DATA DISTRIBUTION", "id": "826b56bc-f4f7-4707-8027-f082ec0f5e7c", "type": "widget"}]
//                 },
//                 "column_name": "education-num",
//                 "column_type": "num",
//                 "stattest_name": "K-S p_value",
//                 "reference_distribution": {
//                     "x": [1.0, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 11.5, 13.0, 14.5, 16.0],
//                     "y": [0.015542211232779936, 0.023972683386318142, 0.08058401036147415, 0.06541858000706464, 0.11628399858707171, 0.0, 0.09706817379018015, 0.07540327328388084, 0.12513834922877665, 0.06725538678912045]
//                 },
//                 "current_distribution": {
//                     "x": [9.0, 9.4, 9.8, 10.2, 10.6, 11.0, 11.4, 11.8, 12.2, 12.6, 13.0],
//                     "y": [1.138984917551319, 0.0, 0.7847156361856423, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5762994462630397]
//                 },
//                 "data_drift": "Detected",
//                 "drift_score": 0.0
//             }
//             ]
//         },
//         "insights": [],
//         "alerts": [],
//         "tabs": [],
//         "widgets": [],
//         "pageSize": 5
//     }
//     ]
// }, new Map(), [{id:"project_1", project_name: "Project #1"}]);

ReactDOM.render(
    <>
        <RouterProvider router={router}/>
    </>,
    document.getElementById('root') as HTMLElement,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
