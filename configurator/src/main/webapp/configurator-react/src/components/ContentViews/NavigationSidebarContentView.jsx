import { Outlet } from "react-router-dom";
import NavigationSidebar from "../Sidebars/BasicNavigationSideBar/BasicNavigationSideBar";
import "./ContentView.css";
import "./NavigationSidebarContentView.css";


const BasicNavigationSidebarContentView = (props) => {
    return (
        // TODO: Cleanup <main> 
        <>
            <main className="content-view">
                <NavigationSidebar navigationLinks={props.navigationLinks}/>
                <Outlet />
            </main>
        </>
    );
}

export default BasicNavigationSidebarContentView;