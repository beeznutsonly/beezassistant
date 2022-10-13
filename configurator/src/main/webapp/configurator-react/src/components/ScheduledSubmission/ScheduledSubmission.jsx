import DateAdapter from '@date-io/date-fns';
import './ScheduledSubmission.css';

const ScheduledSubmission = props => {
    
    const dateAdapter = new DateAdapter();

    return (
        <>
            <div className="scheduled-submission general-list-group-item-content">
                <h2 className="scheduled-submission-title">{props.title}</h2>
                <label className="scheduled-submission-url">{props.url}</label>
                <label className="scheduled-submission-subreddit">r/{props.subreddit}</label>
                <label className="scheduled-submission-time">{
                    dateAdapter.formatByString(dateAdapter.date(props.scheduledTime), 'E, dd MMM yyyy HH:mm O')
                }</label>
            </div>
        </>
    )
}

export default ScheduledSubmission;