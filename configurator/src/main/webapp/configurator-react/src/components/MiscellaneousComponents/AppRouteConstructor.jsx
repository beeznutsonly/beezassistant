import { Route, Routes } from "react-router-dom";
import PageNotFoundContent from "../NavigableContent/PageNotFoundContent";

const AppRouteConstructor = ({
    appView,
    rootContentView,
    nonRootContentView,
    homeNavigable,
    navigables
}) => {

    const unwrapRoute = (navigable, exactPath) => {
        return (
            <Route
                exact={exactPath} path={navigable.path}
                element={navigable.linkContent}
                key={navigable.path}
            >
                { 
                    navigable.subNavigables && 
                    unwrapRoutes(navigable.subNavigables, false)
                }
            </Route>
        );
    }

    const unwrapRoutes = (navigables, exactPaths) => {
        return navigables.map(
            navigable => unwrapRoute(navigable, exactPaths)
        );
    }

    return (
        <Routes>
            <Route 
                exact path="/" 
                element={appView}
            >
                <Route exact path="/" element={rootContentView}>
                    <Route index element={homeNavigable.linkContent} />
                </Route>
                <Route path="/" element={
                    nonRootContentView
                }>
                    {
                        unwrapRoutes(navigables, false)
                    }
                    <Route path="/*" element={<PageNotFoundContent />} />
                </Route>
            </Route>
        </Routes>
    );

}

export default AppRouteConstructor;