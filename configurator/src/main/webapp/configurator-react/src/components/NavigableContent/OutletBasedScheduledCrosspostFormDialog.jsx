import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from '../FormDialogs/OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import ItemModel from '../../models/ScheduledCrosspostModel';
import { useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormControls/DateTimePickerField';
import MediaPreviewCard from '../MediaPreviewCard/MediaPreviewCard';

const OutletBasedScheduledCrosspostFormDialog = (props) => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const [itemModel] = itemModelState;
    const isEditFormState = useState(isEditFormFunction(useLocation(), useParams()));
    const [isEditForm] = isEditFormState;
    const [mediaObject, setMediaObject] = useState();

    return (
        <>
            <OutletBasedFormDialog
                itemModelState={itemModelState}
                isEditFormState={isEditFormState}
                formTitle="Scheduled Crosspost"
                itemFormContent={
                    <div className="v-flexbox">
                        <MediaPreviewCard mediaObject={mediaObject} />
                        <div className="form-fields v-flexbox">
                            <FloatingLabel controlId="title" label="Title">
                                <Form.Control
                                    type="text"
                                    name="title"
                                    placeholder="Title"
                                    onChange={(e) => updateField(e, "title", itemModelState)}
                                    autoComplete="off"
                                    value={getValidFormValue(itemModel.title)}>
                                </Form.Control>
                            </FloatingLabel>
                            <FloatingLabel controlId="url" label="URL">
                                <Form.Control
                                    type="url"
                                    name="url"
                                    placeholder="URL"
                                    inputMode="url"
                                    onChange={(e) => updateField(e, "url", itemModelState)}
                                    onBlur={() => {
                                        if (!isEditForm && itemModel.url) {
                                            props.mediaUrlProcessor.processUrl(
                                                itemModel.url,
                                                setMediaObject
                                            )
                                        }
                                    }}
                                    autoComplete="off"
                                    autoCapitalize="off"
                                    value={getValidFormValue(itemModel.url)}
                                    readOnly={isEditForm}
                                    required>
                                </Form.Control>
                            </FloatingLabel>
                            <FloatingLabel controlId="scheduledTime" label="Scheduled Time">
                                <DateTimePickerField
                                    formItemModelState={itemModelState}
                                    dateTimeFieldName={"scheduledTime"}
                                    inputFormat={'E, dd MMM yyyy HH:mm'}
                                    minDateTime={Date.now()}
                                    inputProps={{
                                        name: "scheduledTime",
                                        placeholder: "Scheduled Time",
                                        autoComplete: "off",
                                        required: true
                                    }}
                                />
                            </FloatingLabel>
                            <FloatingLabel controlId="subreddit" label="Subreddit">
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
                            </FloatingLabel>
                        </div>
                    </div>
                }
            />  
        </>
    );
}

export default OutletBasedScheduledCrosspostFormDialog;