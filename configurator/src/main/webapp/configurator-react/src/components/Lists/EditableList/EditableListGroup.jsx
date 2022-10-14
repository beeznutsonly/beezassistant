import EditableListGroupItem from "./EditableListGroupItem";
import ListGroup from "react-bootstrap/ListGroup";
import EmptyListPlaceholder from "./EmptyListPlaceholder";

const EditableListGroup = (props) => {

    const handleListKeyDown = (event) => {
        if (event.ctrlKey && event.key.toLowerCase() ===  "a") {
            event.preventDefault();
            props.selectAllHandler();
        }
        else if (event.key === "Escape") {
            props.clearSelectionHandler();
        }
        else if (event.key === "Delete") {
            props.removeSelectedHandler();
        }
    }

    return (
        <>
            {
                props.items.length === 0
                ? <EmptyListPlaceholder />
                : <ListGroup onKeyDown={handleListKeyDown}>
                    {(() => {
                        const sortedItems = props.sortingFunctions
                        [props.currentSortingFunction](
                            props.items, props.isSortAscend
                        );
                        const renderedListItems = [];

                        for (let index = 0; index < sortedItems.length; index++) {
                            renderedListItems.push(
                                <EditableListGroupItem 
                                    item={sortedItems[index]}
                                    itemMappingFunction={props.itemMappingFunction}
                                    previousItem={sortedItems[index - 1]}
                                    nextItem={sortedItems[index + 1]}
                                    focusedItemState={props.focusedItemState}
                                    selectedItemsState={props.selectedItemsState}
                                    key={sortedItems[index]._links.self.href}
                                    disabled={props.disabled}
                                />
                            )
                        }
                        return renderedListItems;
                    })()}
                  </ListGroup>
            }
        </>
    );

}

export default EditableListGroup;