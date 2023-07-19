import React, {useState} from "react";
import BaseTabs, {TabInfo} from "./BaseTabs";

/***
 * Provides interactive tabs without needs to control it behavior (ie track active tabs),
 * but all tabs loads from start, so it could be negative on performance
 */

interface AutoTabsProps {
    tabs: TabInfo[];
}

interface AutoTabsState {
    activeTab: number;
}

const AutoTabs: React.FunctionComponent<AutoTabsProps> = (props) => {
    const [state, setState] = useState<AutoTabsState>({activeTab: 0});
    return <React.Fragment>
        <BaseTabs
            activeTab={state.activeTab}
            onNewTabSelected={(_, newTabIdx) => setState(s => ({...s, activeTab: newTabIdx}))}
            tabs={props.tabs}
        />
    </React.Fragment>;
}

export default AutoTabs;