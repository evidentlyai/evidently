import React, {useState} from "react";

import AppBar from "@material-ui/core/AppBar";
import Avatar from "@material-ui/core/Avatar";
import Badge from "@material-ui/core/Badge";
import Breadcrumbs from "@material-ui/core/Breadcrumbs";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import Link from "@material-ui/core/Link";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";

import MenuIcon from "@material-ui/icons/Menu";
import ListIcon from "@material-ui/icons/List";
import NotificationsIcon from '@material-ui/icons/Notifications';

import {makeStyles} from "@material-ui/core/styles";
import SideDrawer from "./SideDrawer";

const useStyles = makeStyles((theme) => ({
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        fontWeight: "normal",
        flexGrow: 1,
    },
    breadcrumbActive: {
        fontWeight: "bold",
    },
    actions: {
        display: "flex",
    },
    action: {
        marginRight: theme.spacing(2),
    }
}));

interface HeaderBarProps {
    path: string[];
    userInfo?: string;
}

interface HeaderBarState {
    drawerOpen: boolean;
}

const HeaderBar: React.FunctionComponent<HeaderBarProps> = (props) => {
    const classes = useStyles();
    const [state, setState] = useState<HeaderBarState>({drawerOpen: false})
    return (<div>
        <AppBar position="static" color="default" variant="outlined">
            <Toolbar variant={"regular"}>
                <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu"
                            onClick={_ => setState(_ => ({drawerOpen: true}))}>
                    <MenuIcon/>
                </IconButton>
                <img src="/evidently_ai_logo_final_web_site.png" alt="" height={56}
                     style={{marginTop: "-18px", marginBottom: "-16px"}}
                />

                <Breadcrumbs aria-label="breadcrumb" color="inherit" className={classes.title}>

                    {props.path.slice(0, props.path.length - 1).map(t =>
                        <Link key={t} color="inherit" href="/">
                            <Typography variant="h6">{t}</Typography>
                        </Link>)}
                    <Typography variant="h6" className={classes.breadcrumbActive} color="inherit">
                        {props.path[props.path.length - 1]}
                    </Typography>
                </Breadcrumbs>
                {props.userInfo
                    ? (<div className={classes.actions}>
                        <div className={classes.action}>
                            <IconButton>
                                <Badge badgeContent={4} color="primary">
                                    <ListIcon/>
                                </Badge>
                            </IconButton>
                            <IconButton>
                                <Badge badgeContent={4} color="primary">
                                    <NotificationsIcon/>
                                </Badge>
                            </IconButton>
                        </div>
                        <Avatar className={classes.action}>{props.userInfo[0]}</Avatar>
                    </div>)
                    : (<Button variant="contained" color="primary" disableElevation href={"https://evidentlyai.com/sign-up"}>Sign Up</Button>)}
            </Toolbar>
        </AppBar>
        <SideDrawer open={state.drawerOpen} onClose={() => setState(_ => ({drawerOpen: false}))}/>
    </div>);
}


export default HeaderBar;