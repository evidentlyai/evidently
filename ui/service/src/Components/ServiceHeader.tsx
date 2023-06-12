import React from "react";

import logo from '../logo.png';
import {AppBar, Button, IconButton, Link, makeStyles, Toolbar, Typography} from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import {GitHub} from "@material-ui/icons";

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

export function ServiceHeader() {
    const classes = useStyles();
    return <>
        <AppBar position={"static"} color={"transparent"}>
            <Toolbar>
                <IconButton edge="start"
                            className={classes.menuButton}
                            color="inherit" aria-label="menu">
                    <MenuIcon/>
                </IconButton>
                <Typography variant="h6"
                            className={classes.title}
                >
                    <img src={logo} height={100} /> <span style={{verticalAlign:"super", fontSize: "0.75rem"}}>0.4.2</span>
                </Typography>
                <Link href={"https://github.com/evidentlyai/evidently"}>
                    <IconButton>
                        <GitHub/>
                    </IconButton>
                </Link>
                <Link href={"https://docs.evidentlyai.com/"}>
                    <Button>Docs</Button>
                </Link>
            </Toolbar>
        </AppBar>
    </>
}