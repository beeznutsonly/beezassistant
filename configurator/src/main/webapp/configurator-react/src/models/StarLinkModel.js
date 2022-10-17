class StarLinkModel {

    constructor (
        linkName,
        link
    ) {
        this.linkName = linkName;
        this.link = link;
    }
    
    static defaultItemModel() {
        return new StarLinkModel("", "");
    }

}

export default StarLinkModel;