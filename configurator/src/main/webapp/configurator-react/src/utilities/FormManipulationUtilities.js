export const getValidFormValue = (value) => {
    return (value === undefined || value === null) ? "" : value;
}

export const updateField = (changeEvent, field, itemModelState) => {
    const itemModel = itemModelState[0];
    const setItemModel = itemModelState[1];
    
    // TODO: Will need to be cleaned up
    changeEvent.preventDefault();
    itemModel[field] = changeEvent.target.value;
    setItemModel(
        {...itemModel}
    );
}

export const isEditForm = (location, params) => {
    const pathNodes = location.pathname.split("/");
    if (pathNodes.includes("edit")) {
        if (location.state) {
            return true;
        }
        else if (params["itemId"]) {
            return true;
        }
    }
    return false;
}

// TODO: Implement
export const cureFormItemModel = (itemModel) => {
    return itemModel
}