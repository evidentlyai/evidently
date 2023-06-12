import React, {useState} from "react";

import Box from "@material-ui/core/Box";
import CircularProgress from "@material-ui/core/CircularProgress";

interface LoadableViewProps<T>
{
    children?: (params: T) => React.ReactNode,
    func: () => Promise<T>,
}

enum LoadState {
    Initialized,
    Loading,
    Loaded,
    Failed,
}

interface LoadableViewState<T> {
    status: LoadState,
    result?: T,
}

const LoadableView = <T,>(props: LoadableViewProps<T>) =>
{
    const [state, setState] = useState<LoadableViewState<T>>(() => ({status: LoadState.Initialized}));
    if (state.status === LoadState.Initialized) {
        setState(_ => ({status: LoadState.Loading}));
        props.func().then(res => setState(s => ({status: LoadState.Loaded, result: res})));
    }

    return <React.Fragment>
        {state.status === LoadState.Loaded
            ? (props.children ? props.children(state.result!) : <div />)
            : <Box textAlign="center"><CircularProgress /></Box>}
    </React.Fragment>;
}

export default LoadableView;