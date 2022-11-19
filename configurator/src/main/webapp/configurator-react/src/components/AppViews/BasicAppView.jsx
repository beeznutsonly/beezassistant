import { Outlet } from "react-router-dom";
import NavigationBar from "../Headers/BasicNavigationBar/BasicNavigationBar";
import "./BasicAppView.css";

const BasicAppView = ({
    theme, 
    title, 
    navigationLinks
}) => {
    return (
        <>
            <div className='app-view'>
                <NavigationBar 
                    theme={theme} 
                    title={title} 
                    navigationLinks={navigationLinks}
                />
                <Outlet />
            </div>
        </>
    )
}

export default BasicAppView;