import { useState } from "react";
import Form from "react-bootstrap/Form";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import ItemModel from "../../models/AdminUpdateModel";
import ItemsRepository from "../../utilities/ItemsRepository";
import BasicFormDialog from "../FormDialogs/BasicFormDialog";
import ItemDialogForm from "../Forms/ItemDialogForm";
import { getValidFormValue, updateField } from "../../utilities/FormManipulationUtilities";

const NewAdminUpdateFormDialog = props => {

    const itemsRepository = new ItemsRepository(props.apiURL + "adminupdates");
    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const isActionInProgressState = useState(false);

    return (
        <>
            <BasicFormDialog 
                form={
                    <ItemDialogForm
                        formTitle={"New Admin Update"}
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
                    </ItemDialogForm>
                }
            />
        </>
    );
}

export default NewAdminUpdateFormDialog;