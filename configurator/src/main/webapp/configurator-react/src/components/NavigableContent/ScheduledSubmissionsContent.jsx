import ItemsRepository from "../../utilities/ItemsRepository";
import ScheduledSubmission from "../ScheduledSubmission/ScheduledSubmission";
import { sortByStrings, sortByTime } from "../../utilities/CommonListSortingFunctions";
import EditableListContent from "./OutletBasedEditableListContent";

const ScheduledSubmissionsContent = () => {
    const itemMappingFunction = scheduledSubmission => {
      return <ScheduledSubmission
          title={scheduledSubmission.title}
          url={scheduledSubmission.url}
          subreddit={scheduledSubmission.subreddit}
          scheduledTime={scheduledSubmission.scheduledTime}
      />
    }
    const itemsRepository = new ItemsRepository(
      window.location.protocol + "//" + window.location.hostname + "/api/scheduledsubmissions"
    );
    const sortingFunctions = {
      "Scheduled Time": (items, isSortAscend) => sortByTime("scheduledTime", items, isSortAscend),
      "Title": (items, isSortAscend) => sortByStrings("title", items, isSortAscend),
      "Subreddit": (items, isSortAscend) => sortByStrings("subreddit", items, isSortAscend)
    };

    return (
      <>
        <EditableListContent 
          itemsRepository={itemsRepository}
          itemMappingFunction={itemMappingFunction}
          sortingFunctions={sortingFunctions}
          shardTitle="Scheduled Submissions"
        />
      </>
    );
  }

export default ScheduledSubmissionsContent;