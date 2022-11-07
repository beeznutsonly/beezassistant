/* eslint-disable jsx-a11y/alt-text */
import { faChevronDown as MenuCollapsed } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useLayoutEffect, useState } from "react";
import Animation from "react-bootstrap/Collapse";
import { Link, NavLink } from "react-router-dom";
import "./BasicNavigationBar.css";

const BasicNavigationBar = (props) => {

    const mql = useState(window.matchMedia('(min-width: 500px)'))[0];
    const [isWidthThreshold, setWidthThreshold] = useState(mql.matches);

    const [isNavigationLinksShown, setNavigationLinksShown] = useState(false);
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

    useLayoutEffect(() => {
        mql.onchange = event => {
            setWidthThreshold(event.matches)
        }
    }, [mql])

    return (
        <>
            <nav className={`basic-navigation-bar ${navigationBarType}`}>
                <div 
                    className="primary-pane"
                >
                    <div 
                        className="menu-selector"
                        onClick={() => setNavigationLinksShown(value => !value)}
                    >
                        {
                            !isNavigationLinksShown
                            ? <FontAwesomeIcon icon={MenuCollapsed} />
                            : <FontAwesomeIcon icon={MenuCollapsed} transform="flip-v"/>
                        }
                    </div>
                    <Link to="/" className="home-icon">
                        <img title="Home" className={logoType} />
                    </Link>
                    <label className="navigation-bar-label">{props.label}</label>
                </div>
                {
                    props.navigationLinks && props.navigationLinks.length > 0
                    ? (
                            isWidthThreshold 
                            ? (
                                <div className="header-navigation-links">
                                    {
                                        props.navigationLinks.map(
                                            navigationLink =>
                                                <NavLink to={navigationLink.path} end key={navigationLink.path}>
                                                    {navigationLink.linkName}
                                                </NavLink>
                                        )
                                    }
                                </div>
                            )
                            : ( 
                                <Animation
                                    in={isNavigationLinksShown}
                                >
                                    <div className="collapsible">
                                        <div className="header-navigation-links">
                                            {
                                                props.navigationLinks.map(
                                                    navigationLink =>
                                                        <NavLink to={navigationLink.path} end key={navigationLink.path}>
                                                            {navigationLink.linkName}
                                                        </NavLink>
                                                )
                                            }
                                        </div>
                                    </div>
                                </Animation>
                            )
                    )
                    : <></>
                }
            </nav>
        </>
     );
}

export default BasicNavigationBar;