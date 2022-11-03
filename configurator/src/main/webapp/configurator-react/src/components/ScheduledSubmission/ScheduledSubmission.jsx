import DateAdapter from '@date-io/date-fns';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useState } from 'react';
import Collapse from 'react-bootstrap/Collapse';
import { faMessage as Comment, faCalendarCheck as Completed } from '@fortawesome/free-regular-svg-icons';
// import { faCircleCheck as Completed } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import "../StandardListItem/StandardListItem.css"
import './ScheduledSubmission.css';

const ScheduledSubmission = ({ item }) => {
    
    const dateAdapter = new DateAdapter();
    const [isCommentBodyOpen, setCommentBodyOpen] = useState(false);

    return (
        <>
            <div className="item general-list-group-item-content">
                <div className="item-core">
                    <div className="item-core-details">
                        <label className="item-title">{item.title}</label>
                        <label className="scheduled-submission-url">{item.url}</label>
                        <label className="scheduled-submission-subreddit">r/{item.subreddit}</label>
                        <label className="scheduled-submission-scheduled-time">{
                            dateAdapter.formatByString(dateAdapter.date(item.scheduledTime), 'E, dd MMM yyyy HH:mm')
                        }</label>
                    </div>
                    <div className="additional-information-pane">
                        {
                            Boolean(item.completed)
                            ? (
                                <div
                                    title={
                                        `Submission was completed ${
                                            dateAdapter.formatByString(
                                                dateAdapter.date(item.completed.completedTime),
                                                'PPPpp'
                                            )
                                        }`
                                    }
                                    className="item-core-icon completed-check"
                                >
                                    <FontAwesomeIcon icon={Completed}/>
                                </div>
                            )
                            : <></>
                        }
                        {
                            Boolean(item.commentBody)
                            ? (
                                <div
                                    className={`item-secondary-details-selector-group ${
                                        isCommentBodyOpen
                                        ? "active"
                                        : ""
                                    }`}
                                >
                                    <div
                                        title="Comment"
                                        className={`item-secondary-details-selector ${
                                            isCommentBodyOpen
                                            ? "active"
                                            : ""
                                        }`}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setCommentBodyOpen(value => !value)
                                        }}
                                    >
                                        <FontAwesomeIcon icon={Comment}/>
                                    </div>
                                </div>
                            )
                            : <></>
                        }
                    </div>
                </div>
                {
                    Boolean(item.commentBody)
                    ?(
                        <div className="item-secondary-details">
                            <Collapse
                                in={isCommentBodyOpen}
                            >
                                <div className="scheduled-submission-comment-body">
                                    <hr/>
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                    >
                                        { item.commentBody }
                                    </ReactMarkdown>
                                </div>
                            </Collapse>
                        </div>
                    )
                    : <></>
                }
            </div>
        </>
    )
}

export default ScheduledSubmission;