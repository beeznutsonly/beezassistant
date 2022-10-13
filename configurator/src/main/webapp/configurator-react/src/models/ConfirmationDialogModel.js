class ConfirmationDialogModel {

    constructor(isShown, body, confirmedCallback) {
        this.isShown = isShown;
        this.body = body;
        this.confirmedCallback = confirmedCallback;
    }

    static defaultConfirmationDialogModel() {
        return new ConfirmationDialogModel(
            false, "", undefined
        );
    }
}

export default ConfirmationDialogModel;