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
        itemsRepository,
        addItemTools,
        editItemTools
    ) {
        this.itemsAPI = itemsRepository
        this.addItemTools = addItemTools;
        this.editItemTools = editItemTools;
    }

}

export default ItemManipulationTools;