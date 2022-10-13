import AlertModel from "../models/AlertModel";
import ConfirmationDialogModel from "../models/ConfirmationDialogModel";
import { delay } from "./GeneralUtilities";

class AlertSystem {

    constructor(alertSetter, confirmationDialogSetter) {
        this.alertSetter = alertSetter;
        this.confirmationDialogSetter = confirmationDialogSetter;
    }

    alert(body, variant, transitory = false, heading="") {
        this.alertSetter(
            new AlertModel(true, variant, heading, body)
        );
        if (transitory) {
            delay(4000, () => this.closeAlert());
        }
    }

    closeAlert() {
        this.alertSetter(
            new AlertModel(false, "", "", "")
        )
    }

    confirm(body, confirmedCallback) {
        this.confirmationDialogSetter(
            new ConfirmationDialogModel(true, body, confirmedCallback)
        )
    }

}

export default AlertSystem;