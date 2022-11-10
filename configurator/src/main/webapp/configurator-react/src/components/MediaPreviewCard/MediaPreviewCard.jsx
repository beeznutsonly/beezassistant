import DateAdapter from '@date-io/date-fns';
import Transition from 'react-bootstrap/Fade';
import "./MediaPreviewCard.css";

const MediaPreviewCard = props => {

    const mediaObject = props.mediaObject;
    const dateAdapter = new DateAdapter();

    return (
        <>
            {
                Boolean(mediaObject) && !Boolean(mediaObject.errorMessage)
                ? (
                    <Transition in={true} appear={true}>
                        <div className="media-preview-card">
                            <div className="media-preview-card-content">
                                {
                                    mediaObject.thumbnail &&
                                    <img
                                        className="thumbnail"
                                        src={mediaObject.thumbnail}
                                        alt="Thumbnail"
                                    />
                                }
                                <div className="information-pane">
                                    {
                                        mediaObject.title &&
                                        <span className="title">{mediaObject.title}</span>
                                    }
                                    {
                                        mediaObject.publishedTime &&
                                        <span className="published-time">Published: {
                                            dateAdapter.formatByString(
                                                dateAdapter.date(mediaObject.publishedTime * 1000),
                                                'E, dd MMM yyyy HH:mm'
                                            )
                                        }</span>
                                    }
                                    {
                                        mediaObject.author && 
                                        <span className="author">Posted By: {mediaObject.author}</span>
                                    }
                                </div>
                            </div>
                        </div>
                    </Transition>
                )
                : <></>
            }
        </>
    )

}

export default MediaPreviewCard;