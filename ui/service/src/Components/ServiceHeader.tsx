import React, {useState} from "react";

import logo from '../logo.png';
import {AppBar, Button, IconButton, Link, makeStyles, Toolbar, Typography} from "@material-ui/core";
import {GitHub} from "@material-ui/icons";
import {Api} from "../lib/api/Api";

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

export function ServiceHeader(props: {api: Api}) {
    const classes = useStyles();
    let [version, setVersion] = useState<string>("...");
    if (version === "...") {
        props.api.getVersion().then(v => setVersion(v.version));
    }
    return <>
        <AppBar position={"static"} color={"transparent"}>
            <Toolbar>
                <Typography variant="h6"
                            className={classes.title}
                >
                    <img src={logo} height={"55px"} /> <span style={{verticalAlign:"super", fontSize: "0.75rem"}}>{version}</span>
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