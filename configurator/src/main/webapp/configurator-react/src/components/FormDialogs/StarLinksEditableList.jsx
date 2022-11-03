import { useState } from "react";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import StarLinkModel from "../../models/StarLinkModel";
import { getValidFormValue, updateField } from "../../utilities/FormManipulationUtilities";
import EditableList from "../Lists/EditableList/EditableList";
import StarLink from "../StarLink/StarLink";

const StarLinksEditableList = (props) => {

    const starLinkModelState = useState(
        new StarLinkModel("", "")
    )
    const [starLinkModel, setStarLinkModel] = starLinkModelState;
    const [itemModel, setItemModel] = props.itemModelState;

    const itemMappingFunction = starLink => (
        <StarLink linkName={starLink.linkName} link={starLink.link}/>
    );

    const addItemHandler = () => {
        setItemModel(currentItemModel => {
                return {
                    ...currentItemModel,
                    starLinks: [...currentItemModel.starLinks, {...starLinkModel}]
                }
        });
    }

    const editItemHandler = (itemToBeEdited) => {
        setStarLinkModel({...itemToBeEdited});
    }

    const removeSelectedHandler = (selectedItems) => {
        setItemModel(currentItemModel => {
                return {
                    ...currentItemModel,
                    starLinks: [...currentItemModel.starLinks.filter(
                        starLink => !selectedItems.has(starLink)
                    )]
                }
        });
    }

    return (
        <div className="v-flexbox">
            <EditableList
                items={itemModel.starLinks}
                addItemHandler={addItemHandler}
                editItemHandler={editItemHandler}
                removeSelectedHandler={removeSelectedHandler}
                itemMappingFunction={itemMappingFunction}
                actionStatuses={{
                    isAddingAvailable: Boolean(starLinkModel.linkName) && Boolean(starLinkModel.link),
                    isEditingAvailable: true,
                    isRemovingAvailable: true,
                    isRefreshingAvailable: false
                }}
                listAdornment={
                    <InputGroup>
                        <Form.Control
                            type="text"
                            placeholder="Link Name"
                            onChange={(e) => updateField(e, "linkName", starLinkModelState)}
                            value={getValidFormValue(starLinkModel.linkName)}>
                        </Form.Control>
                        <Form.Control
                            type="url"
                            inputMode="url"
                            placeholder="Link"
                            onChange={(e) => updateField(e, "link", starLinkModelState)}
                            value={getValidFormValue(starLinkModel.link)}>
                        </Form.Control>
                    </InputGroup>
                }
            />
        </div>
    );
}

export default StarLinksEditableList;