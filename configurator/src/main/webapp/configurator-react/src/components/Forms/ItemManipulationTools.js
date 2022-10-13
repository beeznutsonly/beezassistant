class ItemTools {

    constructor (
        submitSuccessCallback,
        isActionInProgressState
    ) {
        this.submitSuccessCallback = submitSuccessCallback;
        this.isActionInProgressState = isActionInProgressState;
    }

}

export { ItemTools };

class ItemManipulationTools {
    
    constructor (
        itemsAPI,
        addItemTools,
        editItemTools
    ) {
        this.itemsAPI = itemsAPI
        this.addItemTools = addItemTools;
        this.editItemTools = editItemTools;
    }

}

export default ItemManipulationTools;