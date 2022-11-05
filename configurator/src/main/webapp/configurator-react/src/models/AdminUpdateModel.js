class AdminUpdateModel {
    
    constructor(
        heading,
        details
    ) {
        this.heading = heading;
        this.details = details;
    }

    static defaultItemModel() {
        return new AdminUpdateModel("", "");
    }

}

export default AdminUpdateModel;