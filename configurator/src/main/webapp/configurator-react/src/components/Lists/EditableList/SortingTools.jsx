import Dropdown from "react-bootstrap/Dropdown";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { 
    faArrowDownWideShort as Sort, 
    faArrowUpLong as ArrowUp, 
    faArrowDownLong as ArrowDown
} from "@fortawesome/free-solid-svg-icons";
import "./SortingTools.css";

const SortingTools = (props) => {

    const [isSortAscend, setSortAscend] = props.sortAscendState;

    const toggleSortOrder = () => {
        setSortAscend(isSortAscend ? false : true);
    }

    const [currentSortingFunction, setCurrentSortingFunction] = props.currentSortingFunctionState;

    return (
        <div className="sorting-tools btn-group">
            <Dropdown className="sort-dropdown" onSelect={setCurrentSortingFunction}>
                <Dropdown.Toggle className="dropdown-toggle" variant="Primary">
                    <FontAwesomeIcon icon={Sort} />
                    <span className="active-sort">{currentSortingFunction}</span>
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    {
                        [...Object.keys(props.sortingFunctions)].sort().map(sortingFunctionKey =>
                            <Dropdown.Item 
                                href="#" 
                                eventKey={sortingFunctionKey}
                                key={sortingFunctionKey}
                            >
                                {sortingFunctionKey}
                            </Dropdown.Item>
                        )
                    }
                </Dropdown.Menu>
            </Dropdown>
            <button className="btn sort-order-button" onClick={toggleSortOrder}>
                <FontAwesomeIcon icon={
                    isSortAscend ? ArrowUp : ArrowDown
                }/>
            </button>
        </div>
    )
}

export default SortingTools;