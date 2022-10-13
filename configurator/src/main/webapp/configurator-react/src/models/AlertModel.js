class AlertModel {

    constructor(
        isShown,
        variant,
        heading,
        body
    ) {
        this.isShown = isShown;
        this.variant = variant;
        this.heading = heading;
        this.body = body;
    }

    static defaultAlertModel() {
        return new AlertModel(false, undefined, "", "");
    }

}

export default AlertModel;