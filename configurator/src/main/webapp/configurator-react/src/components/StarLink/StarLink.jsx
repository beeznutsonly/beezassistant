import './StarLink.css';

const StarLink = props => {
    return (
        <>
            <div className="star-link general-list-group-item-content">
                <label className="star-link-link-name">{props.linkName}</label>
                <label className="star-link-link">{props.link}</label>
            </div>
        </>
    );
}

export default StarLink;