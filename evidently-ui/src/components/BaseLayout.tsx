import React from "react";
import Box from "@material-ui/core/Box";
import Container from "@material-ui/core/Container";
import {makeStyles} from "@material-ui/core/styles";
import HeaderBar from "./HeaderBar";

const useStyles = makeStyles((theme) => ({
    root: {
        width: "100%",
        padding: 0,
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
    main: {
    },
    breadcrumbActive: {
        fontWeight: "bolder",
    }
}));

export interface BaseLayoutProps {
    path: string[];
}

const BaseLayout : React.FunctionComponent<BaseLayoutProps> = (props) => {
    const classes = useStyles();
    return (
        <Container className={classes.root} maxWidth={false}>
            <HeaderBar path={props.path} userInfo={undefined}/>
            <Box className={classes.main} >
                {props.children}
            </Box>
        </Container>
    );
}

export default BaseLayout;