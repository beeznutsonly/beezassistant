class InlineLoadingAnimationModel {
    
    constructor(
        isShown,
        animation,
        size
    ) {
        this.isShown = isShown;
        this.animation = animation;
        this.size = size;
    }

    static defaultLoadingAnimationModel() {
        return new InlineLoadingAnimationModel(true, "border", "sm")
    }

}

export default InlineLoadingAnimationModel;