import ItemsRepository from "../../utilities/ItemsRepository";
import ScheduledCrosspost from "../ScheduledCrosspost/ScheduledCrosspost";
import { sortByStrings, sortByTime } from "../../utilities/CommonListSortingFunctions";
import EditableListContent from "./OutletBasedEditableListContent";

const ScheduledCrosspostsContent = (props) => {
    const itemMappingFunction = scheduledCrosspost => {
      return <ScheduledCrosspost 
        item={scheduledCrosspost}
        mediaUrlProcessor={props.universalMediaUrlProcessor}
      />
    }
    const itemsRepository = new ItemsRepository(
      props.apiURL +  "scheduledcrossposts"
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
          shardTitle="Scheduled Crossposts"
        />
      </>
    );
  }

export default ScheduledCrosspostsContent;