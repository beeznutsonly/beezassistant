import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from '../FormDialogs/OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import ItemModel from '../../models/ScheduledSubmissionModel';
import { useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormFieldControls/DateTimePickerField';

const OutletBasedScheduledSubmissionFormDialog = () => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const isEditFormState = useState(isEditFormFunction(useLocation(), useParams()));
    const isEditForm = isEditFormState[0];

    return (
        <>
            <OutletBasedFormDialog
                itemModelState={itemModelState}
                isEditFormState={isEditFormState}
                formTitle="Scheduled Submission"
                itemFormContent={
                    <div className="form-fields v-flexbox">
                        <Form.Control
                            type="text"
                            name="title"
                            placeholder="Title"
                            onChange={(e) => updateField(e, "title", itemModelState)}
                            autoComplete="off"
                            value={getValidFormValue(itemModel.title)}
                            required>
                        </Form.Control>
                        <Form.Control
                            type="url"
                            name="url"
                            placeholder="URL"
                            inputMode="url"
                            onChange={(e) => updateField(e, "url", itemModelState)}
                            autoComplete="off"
                            autoCapitalize="off"
                            value={getValidFormValue(itemModel.url)}
                            readOnly={isEditForm}
                            required>
                        </Form.Control>
                        <DateTimePickerField
                            formItemModelState={itemModelState}
                            dateTimeFieldName={"scheduledTime"}
                            inputFormat={'E, dd MMM yyyy HH:mm'}
                            minDateTime={Date.now()}
                            inputProps={{
                                name:"scheduledTime",
                                placeholder: "Scheduled Time",
                                autoComplete: "off",
                                required: true
                            }}
                        />
                        <Form.Control
                            type="text"
                            name="flairId"
                            placeholder="Flair ID"
                            autoCapitalize="off"
                            onChange={(e) => updateField(e, "flairId", itemModelState)}
                            value={getValidFormValue(itemModel.flairId)}
                        >
                        </Form.Control>
                        <Form.Control
                            type="text"
                            name="subreddit"
                            placeholder="Subreddit"
                            autoCapitalize="off"
                            onChange={(e) => updateField(e, "subreddit", itemModelState)}
                            value={getValidFormValue(itemModel.subreddit)}
                            readOnly={isEditForm}
                            required>
                        </Form.Control>
                        <Form.Control
                            as="textarea"
                            type="text"
                            name="commentBody"
                            placeholder="Auto Reply"
                            onChange={(e) => updateField(e, "commentBody", itemModelState)}
                            autoComplete="off"
                            value={getValidFormValue(itemModel.commentBody)}>
                        </Form.Control>
                    </div>
                }
            />
            
        </>
    );
}

export default OutletBasedScheduledSubmissionFormDialog;