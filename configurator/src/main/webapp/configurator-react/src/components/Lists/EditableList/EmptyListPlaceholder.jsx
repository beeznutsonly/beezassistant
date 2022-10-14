import { faTableList as NothingFound } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./EmptyListPlaceholder.css";

const EmptyListPlaceholder = () => {
    return (
        <div className="empty-list-placeholder">
            <div className="message-container">
                <FontAwesomeIcon className="message-container-icon fa-2x" icon={NothingFound}/>
                <label>Nothing here yet</label>
            </div>
        </div>
    );
}

export default EmptyListPlaceholder;