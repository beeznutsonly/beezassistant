import React, { useEffect, useRef, useState } from "react";
import StickyEventListener from "sticky-event-listener";
import EditableListGroup from "./EditableListGroup";
import EditTools from "./EditTools";
import SortingTools from "./SortingTools";
import "./EditableList.css";

const EditableList = (props) => {

    const items = props.items;
    const sortingFunctions = props.sortingFunctions;

    const [currentSortingFunction, setCurrentSortingFunction] = useState(
        Boolean(sortingFunctions) 
        ? Object.keys(sortingFunctions)[0] : undefined
    );

    const [isSortAscend, setSortAscend] = useState(true);
    const [focusedItem, setFocusedItem] = useState(null);
    const [selectedItems, setSelectedItems] = useState(new Set());
    const [isEditPanelStuck, setEditPanelStuck] = useState(false);
    
    const editPanelRef = useRef();
    
    const { 
        isAddAvailable, 
        isRemoveAvailable, 
        isEditAvailable, 
        isRefreshAvailable 
    } = props.actionStatuses;

    const selectAll = () => {
        setSelectedItems(new Set([...items]));
    }

    const clearSelection = () => {
        setSelectedItems(new Set());
    }

    useEffect(() => {
        new StickyEventListener(editPanelRef.current);
        editPanelRef.current.addEventListener('sticky', function(event) {
            setEditPanelStuck(event.detail.stuck);
        });
    }, []);

    useEffect(() => {
        clearSelection();
    }, [items])

    return(
        <div 
            className="editable-list"
        >
                <div className="sticky edit-panel" ref={editPanelRef}>
                    { 
                        Boolean(props.listAdornment)
                        ? props.listAdornment
                        : <></>
                    }
                    <div 
                        className={
                            `primary-toolkit${isEditPanelStuck ? " stuck": ""}`}
                        >
                        {
                            Boolean(sortingFunctions)
                            ? <SortingTools
                                sortAscendState={[isSortAscend, setSortAscend]}
                                sortingFunctions={sortingFunctions}
                                currentSortingFunctionState={
                                    [
                                        currentSortingFunction,
                                        setCurrentSortingFunction
                                    ]
                                }
                            />
                            : <></>
                        }
                        <EditTools
                            selectedItems={selectedItems}
                            focusedItem= {focusedItem}
                            refreshItemsHandler={props.refreshItemsHandler}
                            addItemHandler={props.addItemHandler}
                            editItemHandler={props.editItemHandler}
                            removeSelectedHandler={props.removeSelectedHandler}
                            clearSelectionHandler={clearSelection}
                            actionStatuses={props.actionStatuses}
                        />
                    </div>
                </div>
                <EditableListGroup 
                    items={items}
                    selectAllHandler={selectAll}
                    clearSelectionHandler={clearSelection}
                    removeSelectedHandler={props.removeSelectedHandler}
                    sortingFunctions={sortingFunctions}
                    currentSortingFunction={currentSortingFunction}
                    isSortAscend={isSortAscend}
                    itemMappingFunction={props.itemMappingFunction}
                    focusedItemState={[focusedItem, setFocusedItem]}
                    selectedItemsState={[selectedItems, setSelectedItems]}
                    disabled={isRefreshAvailable || isAddAvailable || isEditAvailable || isRemoveAvailable}
                />
        </div>
    );
}

export default EditableList;