import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from '../FormDialogs/OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import ItemModel from '../../models/StarModel';
import { useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormFieldControls/DateTimePickerField';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import StarLinksEditableList from './StarLinksEditableList';
import './OutletBasedStarFormDialog.css';

const OutletBasedStarFormDialog = () => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const [isEditForm, setEditForm] = useState(
        isEditFormFunction(useLocation(), useParams())
    );

    return (
        <>
            <OutletBasedFormDialog
                itemModelState={itemModelState}
                isEditFormState={[isEditForm, setEditForm]}
                formTitle="Star"
                itemFormContent={
                    <Tabs
                        defaultActiveKey="starDetails"
                    >
                        <Tab
                            eventKey="starDetails" 
                            title="Star Details"
                        >
                            <div className="form-fields v-flexbox">
                                <Form.Control
                                    type="text"
                                    name="name"
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
                                        name: "birthday",
                                        placeholder: "Birthday",
                                        autoComplete: "off"
                                    }}
                                />
                                <Form.Control
                                    type="text"
                                    name="nationality"
                                    placeholder="Nationality"
                                    onChange={(e) => updateField(e, "nationality", itemModelState)}
                                    value={getValidFormValue(itemModel.nationality)}
                                    readOnly={isEditForm}
                                    required>
                                </Form.Control>
                                <Form.Control
                                    type="text"
                                    name="birthPlace"
                                    placeholder="Birth Place"
                                    onChange={(e) => updateField(e, "birthPlace", itemModelState)}
                                    value={getValidFormValue(itemModel.birthPlace)}
                                >
                                </Form.Control>
                                <Form.Control
                                    type="text"
                                    name="yearsActive"
                                    placeholder="Years Active"
                                    autoComplete="off"
                                    onChange={(e) => updateField(e, "yearsActive", itemModelState)}
                                    value={getValidFormValue(itemModel.yearsActive)}>
                                </Form.Control>
                                <Form.Control
                                    as="textarea"
                                    type="text"
                                    name="description"
                                    placeholder="Description"
                                    onChange={(e) => updateField(e, "description", itemModelState)}
                                    autoComplete="off"
                                    value={getValidFormValue(itemModel.description)}>
                                </Form.Control>
                            </div>
                        </Tab>
                        <Tab
                            eventKey="starLinks"
                            title="Star Links"
                        >
                            <StarLinksEditableList
                                itemModelState={itemModelState}
                            />
                        </Tab>
                    </Tabs>
                }
            />
            
        </>
    );
}

export default OutletBasedStarFormDialog;