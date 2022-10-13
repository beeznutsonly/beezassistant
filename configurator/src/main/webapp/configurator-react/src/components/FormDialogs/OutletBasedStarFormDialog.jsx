import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from './OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import ItemModel from '../../models/StarModel';
import { useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormFieldControls/DateTimePickerField';

const OutletBasedStarFormDialog = () => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const isEditFormState = useState(isEditFormFunction(useLocation(), useParams()));
    const isEditForm = isEditFormState[0];

    return (
        <>
            <OutletBasedFormDialog
                itemModelState={itemModelState}
                isEditFormState={isEditFormState}
                formTitle="Star"
                itemFormContent={
                    <div className="form-fields v-flexbox">
                        <Form.Control
                            type="text"
                            placeholder="Name"
                            onChange={(e) => updateField(e, "name", itemModelState)}
                            autoComplete="off"
                            value={getValidFormValue(itemModel.name)}
                            readOnly={isEditForm}
                            required>
                        </Form.Control>
                        <DateTimePickerField
                            formItemModelState={itemModelState}
                            dateTimeFieldName={"birthday"}
                            isDateOnly={true}
                            inputFormat={'PP'}
                            inputProps={{
                                placeholder: "Birthday",
                                autoComplete: "off",
                                required: true
                            }}
                        />
                        <Form.Control
                            type="text"
                            placeholder="Nationality"
                            onChange={(e) => updateField(e, "nationality", itemModelState)}
                            value={getValidFormValue(itemModel.nationality)}
                            readOnly={isEditForm}
                            required>
                        </Form.Control>
                        <Form.Control
                            type="text"
                            placeholder="Birth Place"
                            onChange={(e) => updateField(e, "birthPlace", itemModelState)}
                            value={getValidFormValue(itemModel.birthPlace)}
                        >
                        </Form.Control>
                        <Form.Control
                            type="text"
                            placeholder="Years Active"
                            onChange={(e) => updateField(e, "yearsActive", itemModelState)}
                            value={getValidFormValue(itemModel.yearsActive)}>
                        </Form.Control>
                        <Form.Control
                            as="textarea"
                            type="text"
                            placeholder="Description"
                            onChange={(e) => updateField(e, "description", itemModelState)}
                            autoComplete="off"
                            value={getValidFormValue(itemModel.description)}>
                        </Form.Control>
                    </div>
                }
            />
            
        </>
    );
}

export default OutletBasedStarFormDialog;