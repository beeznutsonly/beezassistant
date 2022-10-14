import DateAdapter from '@date-io/date-fns';

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
        const dateAdapter = new DateAdapter();
        return new ScheduledCrosspostModel("", "", dateAdapter.date(), "");
    }

}

export default ScheduledCrosspostModel;