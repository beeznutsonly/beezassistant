import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { 
    faUndo as Refresh,  
    faAdd as Add,
    faMultiply as Cancel 
} from "@fortawesome/free-solid-svg-icons";
import {
    faTrashCan as Remove, 
    faEdit as Edit,
} from "@fortawesome/free-regular-svg-icons";
import "./EditTools.css";

const EditTools = (props) => {

    const { 
        isRefreshingAvailable, 
        isAddingAvailable, 
        isEditingAvailable, 
        isRemovingAvailable 
    } = props.actionStatuses

    return(
        <>
            <div 
                className="edit-tools btn-group"
            >
                <div 
                    className="selection-manipulation-tools btn-group"
                    style={
                        props.selectedItems.size !== 0
                        ? {
                            display: 'inherit',
                            visibility: 'visible'
                        }
                        : {
                            display: 'none',
                            visibility: 'hidden'
                        }
                    }
                >
                    <button
                        title="Edit"
                        className="btn edit-tools-button edit-button"
                        style={
                            Boolean(props.editItemHandler) && props.selectedItems.size === 1
                            ? {display: 'initial'}
                            : {display: 'none'}
                        }
                        onClick={(e) => {
                            e.preventDefault();
                            props.editItemHandler(props.focusedItem);
                        }}
                        disabled={!(isEditingAvailable && Boolean(props.editItemHandler))}
                    >
                        <FontAwesomeIcon icon={Edit}></FontAwesomeIcon>
                    </button>
                    <button
                        title="Remove"
                        className="btn edit-tools-button remove-button"
                        style={
                            Boolean(props.removeSelectedHandler)
                            ? {display: 'initial'}
                            : {display: 'none'}
                        }
                        onClick={(e) => {
                            e.preventDefault();
                            props.removeSelectedHandler(
                                props.selectedItems
                            );
                        }}
                        disabled={!(isRemovingAvailable && Boolean(props.removeSelectedHandler))}
                    >
                        <FontAwesomeIcon icon={Remove}></FontAwesomeIcon>
                    </button>
                    <button className="btn edit-tools-button cancel-button" onClick={(e) => {
                        e.preventDefault();
                        props.clearSelectionHandler();
                    }}>
                        <FontAwesomeIcon icon={Cancel}></FontAwesomeIcon>
                    </button>
                </div>
                <button 
                    className="btn edit-tools-button add-item-button" 
                    style={
                        Boolean(props.addItemHandler)
                        ? {display: 'inherit'}
                        : {display: 'none'}
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        props.addItemHandler();
                    }}
                    disabled={!(isAddingAvailable && Boolean(props.addItemHandler))}
                >
                    <FontAwesomeIcon icon={Add}></FontAwesomeIcon>
                </button>
                <button 
                    className="btn edit-tools-button refresh-button" 
                    style={
                        Boolean(props.refreshItemsHandler)
                        ? {display: 'inherit'}
                        : {display: 'none'}
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        props.refreshItemsHandler();
                    }}
                    disabled={!(isRefreshingAvailable && Boolean(props.refreshItemsHandler))}
                >
                    <FontAwesomeIcon icon={Refresh}></FontAwesomeIcon>
                </button>
            </div>
        </>
    )
}

export default EditTools;