class ScheduledCrosspostModel {
    
    constructor(
        title,
        url,
        scheduledTime,
        subreddit
    ) {
        this.title = title;
        this.url = url;
        this.scheduledTime = scheduledTime;
        this.subreddit = subreddit;
    }

    static defaultItemModel() {
        return new ScheduledCrosspostModel("", "", Date.now(), "");
    }

}

export default ScheduledCrosspostModel;