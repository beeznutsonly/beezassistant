import DateAdapter from '@date-io/date-fns';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import "../StandardListItem/StandardListItem.css"
import "./Star.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLink as Links } from '@fortawesome/free-solid-svg-icons';
import { faCircleUser as Description } from '@fortawesome/free-regular-svg-icons';
import Collapse from 'react-bootstrap/Collapse';
import { useState } from 'react';

const Star = ({ item }) => {

    const dateAdapter = new DateAdapter();

    const [isDescriptionOpen, setDescriptionOpen] = useState(false);
    const [isStarLinksOpen, setStarLinksOpen] = useState(false);

    return (
        <>
            <div className="item general-list-group-item-content">
                <div className="item-core">
                    <div className="item-core-details">
                        <h2 className="item-title">{item.name}</h2>
                        <label className="star-birthday">{
                            Boolean(item.birthday)
                            ? dateAdapter.formatByString(dateAdapter.date(item.birthday), 'PP')
                            : item.birthday
                        }</label>
                        <label className="star-nationality">Nationality: {item.nationality}</label>
                        <label className="star-birth-place">Birth Place: {item.birthPlace}</label>
                        <label className="star-years-active">Years Active: {item.yearsActive}</label>
                    </div>
                    <div className="additional-information-pane">
                        {
                            Boolean(item.description) || Boolean(item.starLinks.length)
                            ?(
                                <div
                                    className={`item-secondary-details-selector-group ${
                                        isDescriptionOpen || isStarLinksOpen
                                        ? "active"
                                        : ""
                                    }`}
                                >
                                    {Boolean(item.description)
                                    ?(
                                        <div
                                            title="Bio"
                                            className={
                                                `item-core-icon item-secondary-details-selector ${
                                                    isDescriptionOpen
                                                    ? "active"
                                                    : ""
                                                }`
                                            }
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setDescriptionOpen(value => !value)
                                            }}
                                        >
                                            <FontAwesomeIcon icon={Description}/>
                                        </div>
                                    )
                                    : <></>}
                                    {Boolean(item.starLinks.length)
                                    ?(
                                        <div
                                            title="Links"
                                            className={
                                                `item-core-icon item-secondary-details-selector ${
                                                    isStarLinksOpen
                                                    ? "active"
                                                    : ""
                                                }`
                                            }
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setStarLinksOpen(value => !value)
                                            }}
                                        >
                                            <FontAwesomeIcon icon={Links}/>
                                        </div>
                                    )
                                    : <></>}
                                </div>
                            )
                            : <></>
                        }
                    </div>
                </div>
                {
                    Boolean(item.description) || Boolean(item.starLinks.length)
                    ? (
                        <div className="item-secondary-details">
                            {Boolean(item.description)
                                ?(
                                    <Collapse
                                        in={isDescriptionOpen}
                                    >
                                        <div className='star-description'>
                                            <hr/>
                                            <ReactMarkdown 
                                                remarkPlugins={[remarkGfm]}
                                            >
                                                { item.description }
                                            </ReactMarkdown>
                                        </div>
                                    </Collapse>
                                )
                                : <></>}
                            {Boolean(item.starLinks.length)
                                ?(
                                    <Collapse
                                        in={isStarLinksOpen}
                                    >
                                        <div className="star-links">
                                            <hr/>
                                            <ul>
                                                {
                                                    item.starLinks.map(starLink => (
                                                        <li key={
                                                            `${starLink.linkName}__${starLink.link}`
                                                        }>
                                                            <a 
                                                                rel="noreferrer"
                                                                href={starLink.link}
                                                                target="_blank"
                                                            >
                                                                {
                                                                    starLink.linkName
                                                                    ? starLink.linkName
                                                                    : <></>
                                                                }
                                                            </a>
                                                        </li>
                                                    ))
                                                }
                                            </ul>
                                        </div>
                                    </Collapse>
                                )
                                : <></>}
                        </div>
                    )
                    : <></>
                }
            </div>
        </>
    );
}

export default Star;