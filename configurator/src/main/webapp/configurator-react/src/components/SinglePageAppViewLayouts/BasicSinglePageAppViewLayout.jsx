import { Outlet } from "react-router-dom";
import Header from "../Headers/BasicNavigationBar/BasicNavigationBar";
import "./BasicSinglePageAppViewLayout.css";

const BasicSinglePageAppViewLayout = (props) => {
    return (
        <>
            <div className='app-view'>
                <Header 
                    theme={props.theme} 
                    label={props.label} 
                    navigationLinks={props.navigationLinks}
                />
                <Outlet />
            </div>
        </>
    )
}

export default BasicSinglePageAppViewLayout;