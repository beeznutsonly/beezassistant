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

const EditTools = ({
    actionStatuses,
    selectedItems,
    focusedItem,
    addItemHandler,
    editItemHandler,
    removeSelectedHandler,
    refreshItemsHandler,
    clearSelectionHandler
}) => {

    const { 
        isRefreshingAvailable, 
        isAddingAvailable, 
        isEditingAvailable, 
        isRemovingAvailable 
    } = actionStatuses

    return(
        <>
            <div 
                className="edit-tools btn-group"
            >
                <div 
                    className="selection-manipulation-tools btn-group"
                    style={
                        selectedItems.size !== 0
                        ? { display: 'contents' }
                        : { display: 'none' }
                    }
                >
                    {
                        focusedItem && 
                        !(focusedItem.isEditable === false) &&
                        <button
                            title="Edit"
                            className="btn edit-tools-button edit-button"
                            style={
                                Boolean(editItemHandler) && selectedItems.size === 1
                                ? {display: 'initial'}
                                : {display: 'none'}
                            }
                            onClick={(e) => {
                                e.preventDefault();
                                editItemHandler(focusedItem)
                            }}
                            disabled={!(isEditingAvailable && Boolean(editItemHandler))}
                        >
                            <FontAwesomeIcon icon={Edit}></FontAwesomeIcon>
                        </button>
                    }
                    <button
                        title="Remove"
                        className="btn edit-tools-button remove-button"
                        style={
                            Boolean(removeSelectedHandler)
                            ? {display: 'initial'}
                            : {display: 'none'}
                        }
                        onClick={(e) => {
                            e.preventDefault();
                            removeSelectedHandler(
                                selectedItems
                            );
                        }}
                        disabled={!(isRemovingAvailable && Boolean(removeSelectedHandler))}
                    >
                        <FontAwesomeIcon icon={Remove}></FontAwesomeIcon>
                    </button>
                    <button 
                        className="btn edit-tools-button cancel-button" 
                        onClick={(e) => {
                            e.preventDefault();
                            clearSelectionHandler();
                        }}
                    >
                        <FontAwesomeIcon icon={Cancel}></FontAwesomeIcon>
                    </button>
                </div>
                <button 
                    className="btn edit-tools-button add-item-button" 
                    style={
                        Boolean(addItemHandler)
                        ? {display: 'inherit'}
                        : {display: 'none'}
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        addItemHandler();
                    }}
                    disabled={!(isAddingAvailable && Boolean(addItemHandler))}
                >
                    <FontAwesomeIcon icon={Add}></FontAwesomeIcon>
                </button>
                <button 
                    className="btn edit-tools-button refresh-button" 
                    style={
                        Boolean(refreshItemsHandler)
                        ? {display: 'inherit'}
                        : {display: 'none'}
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        refreshItemsHandler();
                    }}
                    disabled={!(isRefreshingAvailable && Boolean(refreshItemsHandler))}
                >
                    <FontAwesomeIcon icon={Refresh}></FontAwesomeIcon>
                </button>
            </div>
        </>
    )
}

export default EditTools;