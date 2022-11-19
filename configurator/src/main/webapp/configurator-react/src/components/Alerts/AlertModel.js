export default class AlertModel {

    constructor(
        isShown,
        variant,
        body,
        heading
    ) {
        this.isShown = isShown;
        this.variant = variant;
        this.body = body;
        this.heading = heading;
    }

    static defaultModel() {
        return new AlertModel(false, undefined, "", "");
    }

}