import React, { useEffect, useState } from "react";
import EditableListGroup from "./EditableListGroup";
import EditTools from "./EditTools";
import SortingTools from "./SortingTools";
import "./EditableList.css";

const EditableList = (props) => {

    const items = props.items;
    const sortingFunctions = props.sortingFunctions;

    const [currentSortingFunction, setCurrentSortingFunction] = useState(
        Object.keys(sortingFunctions)[0]
    );
    const [isSortAscend, setSortAscend] = useState(true);
    const [focusedItem, setFocusedItem] = useState(null);
    const [selectedItems, setSelectedItems] = useState(new Set());
    
    const { isAdding, isRemoving, isEditing, isRefreshing } = props.actionStatuses;

    const selectAll = () => {
        setSelectedItems(new Set([...items]));
    }

    const clearSelection = () => {
        setSelectedItems(new Set());
    }

    useEffect(() => {
        clearSelection();
    }, [items])

    return(
        <div 
            className="editable-list"
        >
                <div className="edit-panel">
                    <SortingTools 
                        sortAscendState={[isSortAscend, setSortAscend]}
                        sortingFunctions={sortingFunctions}
                        currentSortingFunctionState={
                            [
                                currentSortingFunction,
                                setCurrentSortingFunction
                            ]
                        }
                    />
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
                    disabled={isRefreshing || isAdding || isEditing || isRemoving}
                />
        </div>
    );
}

export default EditableList;