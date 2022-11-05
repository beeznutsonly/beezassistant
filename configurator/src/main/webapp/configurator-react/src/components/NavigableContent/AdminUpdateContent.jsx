import { useState } from "react";
import Form from "react-bootstrap/Form";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import ItemModel from "../../models/AdminUpdateModel";
import ItemsRepository from "../../utilities/ItemsRepository";
import ItemForm from "../Forms/ItemForm";
import { getValidFormValue, updateField } from "../../utilities/FormManipulationUtilities";
import ContentShard from "../ContentShards/StandardContentShard";
import "./AdminUpdateContent.css";

const AdminUpdateContent = (props) => {

    const itemsRepository = new ItemsRepository(props.apiURL + "adminupdates");
    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const isActionInProgressState = useState(false);

    return (
        <>
            <ContentShard title={"New Admin Update"}>
                <ItemForm
                    className="admin-update-content-form"
                    itemModel={itemModel}
                    isActionInProgressState={isActionInProgressState}
                    itemAPIAction={(item) => itemsRepository.addItem(item)}
                    successMessage={
                        `Admin update successfully posted`
                    }
                    failureMessage={
                        `Failed to post admin update`
                    }
                >
                    <div className="form-fields v-flexbox">
                        <FloatingLabel controlId="heading" label="Heading">
                            <Form.Control
                                type="text"
                                name="heading"
                                placeholder="Heading"
                                onChange={(e) => updateField(e, "heading", itemModelState)}
                                autoComplete="off"
                                value={getValidFormValue(itemModel.heading)}
                                required>
                            </Form.Control>
                        </FloatingLabel>
                        <FloatingLabel controlId="details" label="Details">
                            <Form.Control
                                className="details-field"
                                as="textarea"
                                type="textarea"
                                name="details"
                                placeholder="Details"
                                onChange={(e) => updateField(e, "details", itemModelState)}
                                autoComplete="off"
                                value={getValidFormValue(itemModel.details)}
                                required>
                            </Form.Control>
                        </FloatingLabel>
                    </div>
                </ItemForm>
            </ContentShard>
        </>
    );
}

export default AdminUpdateContent;