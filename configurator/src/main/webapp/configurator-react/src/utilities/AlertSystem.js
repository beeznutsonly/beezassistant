import ConfirmationDialogModel from "../models/ConfirmationDialogModel";
import { delay } from "./GeneralUtilities";

class AlertSystem {

    constructor(alertController, confirmationDialogSetter) {
        this.alertController = alertController;
        this.confirmationDialogSetter = confirmationDialogSetter;
    }

    alert(body, variant, transitory = false, heading="") {
        this.alertController.openAlert(
            variant, body, heading
        );
        if (transitory) {
            delay(4000, () => this.alertController.closeAlert());
        }
    }

    confirm(body, confirmedCallback) {
        this.confirmationDialogSetter(
            new ConfirmationDialogModel(true, body, confirmedCallback)
        )
    }

}

export default AlertSystem;