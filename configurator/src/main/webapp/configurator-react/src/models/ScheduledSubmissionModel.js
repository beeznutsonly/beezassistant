class ScheduledSubmissionModel {
    
    constructor(
        title,
        url,
        scheduledTime,
        flairId,
        subreddit,
        commentBody
    ) {
        this.title = title;
        this.url = url;
        this.scheduledTime =scheduledTime;
        this.flairId = flairId;
        this.subreddit = subreddit;
        this.commentBody = commentBody;
    }

    static defaultItemModel() {
        return new ScheduledSubmissionModel("", "", Date.now(), "", "", "");
    }

}

export default ScheduledSubmissionModel;