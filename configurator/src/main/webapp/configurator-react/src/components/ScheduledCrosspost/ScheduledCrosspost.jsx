import DateAdapter from '@date-io/date-fns'
import './ScheduledCrosspost.css';

const ScheduledCrosspost = props => {

    const dateAdapter = new DateAdapter();

    return (
        <>
            <div className="scheduled-crosspost general-list-group-item-content">
                {
                    (props.title === undefined || props.title === null)
                    ? <h2 className="scheduled-crosspost-title scheduled-crosspost-default-title">
                        Original submission title
                    </h2>
                    : <h2 className="scheduled-crosspost-title">{props.title}</h2>
                }
                <label className="scheduled-crosspost-url">{props.url}</label>
                <label className="scheduled-crosspost-subreddit">r/{props.subreddit}</label>
                <label className="scheduled-crosspost-time">{
                    dateAdapter.formatByString(dateAdapter.date(props.scheduledTime), 'E, dd MMM yyyy HH:mm O')
                }</label>
            </div>
        </>
    )
}

export default ScheduledCrosspost;