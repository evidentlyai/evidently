import React, {useState} from "react";

import Box from "@material-ui/core/Box";
import CircularProgress from "@material-ui/core/CircularProgress";

import BaseLayout, {BaseLayoutProps} from "./BaseLayout";

enum LoadingState {
    Created,
    Loading,
    Loaded,
    Failed,
}

interface LoadingLayoutProps<T> extends BaseLayoutProps {
    provider: Promise<T>;
    children?: (params: T) => React.ReactNode;
}

interface LoadingLayoutState<T> {
    state: LoadingState;
    result?: T;
}

const LoadingComponent = <T, >(props: LoadingLayoutProps<T>) => {
    const [state, setState] = useState<LoadingLayoutState<T>>({state: LoadingState.Created})
    if (state.state === LoadingState.Created) {
        props.provider.then(t => setState(_ => ({state: LoadingState.Loaded, result: t})));
        setState(t => t.state === LoadingState.Created ? ({state: LoadingState.Loading}) : t);
    }
    return <React.Fragment>
        {state.state === LoadingState.Loaded ? (props.children ? props.children(state.result!) : <div/>) :
        state.state === LoadingState.Loading ?
            <BaseLayout path={[...props.path, "..."]}>
                <Box textAlign="center">
                    <CircularProgress/>
                </Box>
            </BaseLayout> : <Box textAlign="center">
                Failed to load project data
            </Box>}
    </React.Fragment>
}

export default LoadingComponent;