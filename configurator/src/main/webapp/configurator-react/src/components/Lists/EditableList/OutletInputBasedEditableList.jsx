import { Outlet, useNavigate } from 'react-router-dom';
import ItemsRepository from '../../../utilities/ItemsRepository';
import EditableList from './EditableList';

const OutletInputBasedEditableList = (props) => {
    
    const navigator = useNavigate();

    const removeSelectedHandler = (items) => {
        props.removeSelectedHandler(items);
    }

    const addItemHandler = () => {
        navigator('add');
    }

    const editItemHandler = (item) => {
        navigator(`edit/${ItemsRepository.getItemId(item)}`, { state : item });
    }

    const refreshItemsHandler = () => {
        props.refreshItemsHandler();
    }

    return (
        <>
            <Outlet context={
                props.itemManipulationTools
            }/>
            <EditableList 
                items={props.items}
                refreshItemsHandler={refreshItemsHandler}
                addItemHandler={addItemHandler}
                editItemHandler={editItemHandler}
                removeSelectedHandler={removeSelectedHandler}
                sortingFunctions={props.sortingFunctions}
                itemMappingFunction={props.itemMappingFunction}
                actionStatuses={props.actionStatuses}
            />
        </>
    );
}

export default OutletInputBasedEditableList;