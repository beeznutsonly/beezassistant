import DateAdapter from '@date-io/date-fns';
import { faCalendarCheck as Completed } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import '../StandardListItem/StandardListItem.css';
import './ScheduledCrosspost.css';

const ScheduledCrosspost = ({ item }) => {

    const dateAdapter = new DateAdapter();
    
    return (
        <>
            <div className="item general-list-group-item-content">
                <div className="item-core">
                    <div className="item-core-details">
                        {
                            <label className={
                                `item-title ${
                                    !Boolean(item.title)
                                    ? 'scheduled-crosspost-default-title'
                                    : ''
                                }`
                            }>
                                {
                                    Boolean(item.title)
                                    ? item.title
                                    : "Original submission title"
                                }
                            </label>
                        }
                        <label className="scheduled-crosspost-url">{item.url}</label>
                        <label className="scheduled-crosspost-subreddit">r/{item.subreddit}</label>
                        <label className="scheduled-crosspost-scheduled-time">{
                            dateAdapter.formatByString(dateAdapter.date(item.scheduledTime), 'E, dd MMM yyyy HH:mm')
                        }</label>
                    </div>
                    <div className="additional-information-pane">
                        {
                            Boolean(item.completed)
                            ? (
                                <div
                                    title={
                                        `Crosspost was completed ${
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
                    </div>
                </div>
                
            </div>
        </>
    )
}

export default ScheduledCrosspost;