import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { 
    faUndo as Refresh,  
    faAdd as Add, 
    faEdit as Edit,
    faTrashCan as Remove, 
    faMultiply as Cancel 
} from "@fortawesome/free-solid-svg-icons";
import "./EditTools.css";

const EditTools = (props) => {

    const { isRefreshing, isAdding, isEditing, isRemoving } = props.actionStatuses

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
                            display: 'initial',
                            visibility: 'visible'
                        }
                        : {
                            display: 'none',
                            visibility: 'hidden'
                        }
                    }
                >
                    <button
                        className="btn edit-tools-button remove-button"
                        style={
                            Boolean(props.editItemHandler) && props.selectedItems.size === 1
                            ? {display: 'initial'}
                            : {display: 'none'}
                        }
                        onClick={() => props.editItemHandler(props.focusedItem)}
                        disabled={isEditing || !Boolean(props.editItemHandler)}
                    >
                        <FontAwesomeIcon icon={Edit}></FontAwesomeIcon>
                    </button>
                    <button
                        className="btn edit-tools-button remove-button"
                        style={
                            Boolean(props.removeSelectedHandler)
                            ? {display: 'initial'}
                            : {display: 'none'}
                        }
                        onClick={() => props.removeSelectedHandler(
                            props.selectedItems
                        )}
                        disabled={isRemoving || !Boolean(props.removeSelectedHandler)}
                    >
                        <FontAwesomeIcon icon={Remove}></FontAwesomeIcon>
                    </button>
                    <button className="btn edit-tools-button cancel-button" onClick={() => props.clearSelectionHandler()}>
                        <FontAwesomeIcon icon={Cancel}></FontAwesomeIcon>
                    </button>
                </div>
                <button 
                    className="btn edit-tools-button add-item-button" 
                    style={
                        Boolean(props.addItemHandler)
                        ? {display: 'initial'}
                        : {display: 'none'}
                    }
                    onClick={() => props.addItemHandler()}
                    disabled={isAdding || !Boolean(props.addItemHandler)}
                >
                    <FontAwesomeIcon icon={Add}></FontAwesomeIcon>
                </button>
                <button 
                    className="btn edit-tools-button refresh-button" 
                    style={
                        Boolean(props.refreshItemsHandler)
                        ? {display: 'initial'}
                        : {display: 'none'}
                    }
                    onClick={() => props.refreshItemsHandler()}
                    disabled={isRefreshing || !Boolean(props.refreshItemsHandler)}
                >
                    <FontAwesomeIcon icon={Refresh}></FontAwesomeIcon>
                </button>
            </div>
        </>
    )
}

export default EditTools;