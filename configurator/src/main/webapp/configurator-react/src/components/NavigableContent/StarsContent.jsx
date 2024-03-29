import ItemsRepository from "../../utilities/ItemsRepository";
import Star from "../Star/Star";
import { sortByStrings, sortByTime } from "../../utilities/CommonListSortingFunctions";
import EditableListContent from "./OutletBasedEditableListContent";

const StarsContent = (props) => {
    const itemMappingFunction = star => {
      return <Star item={star}/>
    }
    const itemsRepository = new ItemsRepository(
      props.apiURL + "stars"
    );
    const sortingFunctions = {
      "Name": (items, isSortAscend) => sortByStrings("name", items, isSortAscend),
      "Birthday": (items, isSortAscend) => sortByTime("birthday", items, isSortAscend),
      "Nationality": (items, isSortAscend) => sortByStrings("nationality", items, isSortAscend),
      "Birth Place": (items, isSortAscend) => sortByStrings("birthPlace", items, isSortAscend),
      "Years Active": (items, isSortAscend) => sortByStrings("yearsActive", items, isSortAscend),
    };

    return (
      <>
        <EditableListContent 
          itemsRepository={itemsRepository}
          itemMappingFunction={itemMappingFunction}
          sortingFunctions={sortingFunctions}
          shardTitle="Stars"
        />
      </>
    );
  }

export default StarsContent;