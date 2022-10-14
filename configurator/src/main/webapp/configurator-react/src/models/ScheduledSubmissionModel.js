import DateAdapter from '@date-io/date-fns';

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
        this.scheduledTime = scheduledTime;
        this.flairId = flairId;
        this.subreddit = subreddit;
        this.commentBody = commentBody;
    }

    static defaultItemModel() {
        const dateAdapter = new DateAdapter();
        return new ScheduledSubmissionModel("", "", dateAdapter.date(), "", "", "");
    }

}

export default ScheduledSubmissionModel;