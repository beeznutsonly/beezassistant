import { NavLink } from "react-router-dom";
import "./BasicNavigationSideBar.css";

const BasicNavigationSideBar = props => {
    return (
        <>
            <nav className="navigation-side-bar">
                <ul className="navigation-links">
                    {props.navigationLinks.map(navigationLink => 
                        <NavLink to={navigationLink.path} end key={navigationLink.path}>
                            {navigationLink.linkName}
                        </NavLink>
                    )}
                </ul>
            </nav>
        </>
    )
}

export default BasicNavigationSideBar;