/* eslint-disable jsx-a11y/alt-text */
import { Link } from "react-router-dom";
import "./BasicNavigationBar.css";

const BasicNavigationBar = (props) => {
    
    let navigationBarType, logoType;

    if ((props.theme) === "accent") {
        navigationBarType = "basic-navigation-bar-accent";
        logoType = "logo-light";
    }
    else if ((props.theme) === "light") {
        navigationBarType = "basic-navigation-bar-light"
        logoType = "logo";
    }
    else if ((props.theme) === "dark") {
        navigationBarType = "basic-navigation-bar-dark"
        logoType = "logo-light";
    }

    // eslint-disable-next-line jsx-a11y/alt-text
    return (
        <>
            <nav className={`basic-navigation-bar ${navigationBarType}`}>
                <Link to="/">
                    <img className={logoType} />
                </Link>
                <label className="navigation-bar-label">{props.label}</label>
            </nav>
        </>
     );
}

export default BasicNavigationBar;