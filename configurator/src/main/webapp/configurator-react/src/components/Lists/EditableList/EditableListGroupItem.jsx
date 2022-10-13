import { useEffect, useRef } from "react";
import ListGroup from "react-bootstrap/ListGroup";
import "./EditableListGroupItem.css";

const EditableListGroupItem = (props) => {

    const item = props.item;
    const itemElement = useRef(null);
    const previousItem = props.previousItem;
    const nextItem = props.nextItem;
    const [focusedItem, setFocusedItem] = props.focusedItemState;
    const [selectedItems, setSelectedItems] = props.selectedItemsState;

    const isActive = (item) => {
        return selectedItems.has(item);
    }

    const selectItem = (item, clearSelection)  => {
        if (clearSelection){
            setSelectedItems(new Set([item]));
        }
        else {
           setSelectedItems(new Set([...selectedItems, item]));
        }
        setFocusedItem(item);
    }

    const deselectItem = (item) => {
        selectedItems.delete(item); 
        setSelectedItems(new Set([...selectedItems]));
        setFocusedItem(item);
    }

    const handleListItemClick = (event) =>  {
        event.preventDefault();
        if (event.ctrlKey) {
            if (isActive(item)) {
                deselectItem(item);
            }
            else {
                selectItem(item, false);
            }
        }
        else {
            selectItem(item, true);
        }
    }

    const handleListItemKeydown = (event) => {
        if (event.key === "ArrowUp" || event.key === "ArrowDown") {
            if (event.shiftKey) {
               event.preventDefault();
            }
            
            switch (event.key) {
                case "ArrowUp":
                    if (previousItem) {
                        selectItem(
                            previousItem,
                            !event.shiftKey
                        );
                    }
                    else {
                        selectItem(
                            item,
                            !event.shiftKey
                        );
                    }
                    break;
                case "ArrowDown":
                    if (nextItem) {
                        selectItem(
                            nextItem,
                            !event.shiftKey
                        );
                    }
                    else {
                        selectItem(
                            item,
                            !event.shiftKey
                        );
                    }
                    break;
                default:
                    return;
            }
        }
    }

    useEffect(() => {
        if (Object.is(item, focusedItem)) {
            itemElement.current.focus();
        }
    }, [item, focusedItem]);

    return (
        <>
            <ListGroup.Item 
                action
                active={selectedItems.has(item)}
                onClick={handleListItemClick}
                onKeyDown={handleListItemKeydown}
                disabled={props.disabled}
                ref={itemElement}
            >
                {props.itemMappingFunction(item)}
            </ListGroup.Item>
        </>
    );
}

export default EditableListGroupItem;