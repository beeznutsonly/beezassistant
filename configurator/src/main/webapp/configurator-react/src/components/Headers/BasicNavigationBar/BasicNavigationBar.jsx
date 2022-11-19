/* eslint-disable jsx-a11y/alt-text */
import { faChevronDown as MenuCollapsed } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useLayoutEffect, useState } from "react";
import Animation from "react-bootstrap/Collapse";
import { Link, NavLink } from "react-router-dom";
import "./BasicNavigationBar.css";

const WIDTH_BREAKPOINT = "(min-width: 500px)";

const BasicNavigationBar = ({
    theme,
    title,
    navigationLinks
}) => {

    const widthMediaQueryList = useState(window.matchMedia(WIDTH_BREAKPOINT))[0];
    const [isWidthThreshold, setWidthThreshold] = useState(widthMediaQueryList.matches);

    const [isNavigationLinksShown, setNavigationLinksShown] = useState(false);
    let navigationBarType, logoType;

    const navigationLinkElements = navigationLinks.map(
        navigationLink => (
            <NavLink to={navigationLink.path} end key={navigationLink.path}>
                {navigationLink.linkName}
            </NavLink>
        )
    )

    if (theme === "accent") {
        navigationBarType = "basic-navigation-bar-accent";
        logoType = "logo-light";
    }
    else if (theme === "light") {
        navigationBarType = "basic-navigation-bar-light"
        logoType = "logo";
    }
    else if (theme === "dark") {
        navigationBarType = "basic-navigation-bar-dark"
        logoType = "logo-light";
    }

    useLayoutEffect(() => {
        widthMediaQueryList.onchange = event => {
            setWidthThreshold(event.matches)
        }
    }, [widthMediaQueryList])

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
                    <span className="navigation-bar-label">{title}</span>
                </div>
                {
                    navigationLinks && navigationLinks.length > 0
                    ? (
                            isWidthThreshold 
                            ? (
                                <div className="header-navigation-links">
                                    { 
                                        navigationLinkElements
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
                                                navigationLinkElements
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