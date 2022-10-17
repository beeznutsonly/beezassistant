import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from './OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import ItemModel from '../../models/StarModel';
import { useEffect, useState } from 'react';
import { useLocation, useOutletContext, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormFieldControls/DateTimePickerField';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import './OutletBasedStarFormDialog.css';
import ItemsRepository from '../../utilities/ItemsRepository';
import StarLinksEditableList from './StarLinksEditableList';

const OutletBasedStarFormDialog = () => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const isEditFormState = useState(isEditFormFunction(useLocation(), useParams()));
    const isEditForm = isEditFormState[0];
    const starLinksState = useState([]);
    const [starLinks, setStarLinks] = starLinksState;
    const starLinksPendingRemovalState = useState(new Set());

    const starSubmitSuccessCallback = (star) => {
        const starStarLinksRepository = new ItemsRepository(
            star._links.starLinks
        )
        if (isEditForm) {
            starLinksPendingRemovalState[0].forEach(
                starLinkPendingRemoval => starStarLinksRepository.removeItem(
                    starLinkPendingRemoval
                )
                .catch((error) => {
                    return Promise.reject(new Error(error))
                })
            )
            starLinksPendingRemovalState[1](
                new Set()
            );
        }
        starLinks.forEach(
            starLink => starStarLinksRepository.addItem(
                starLink
            )
            .catch((error) => {
                return Promise.reject(new Error(error))
            })
        )
    }

    useOutletContext().secondarySuccessCallback = starSubmitSuccessCallback;

    useEffect(() => {
        if (isEditForm && itemModel._links) {
            const starStarLinksRepository = new ItemsRepository(
                itemModel._links.starLinks.href
            )
            starStarLinksRepository.retrieveItems()
            .then((response) => {
                if (response.ok) {
                    return response.json()
                }
                return Promise.reject(new Error(response.status))
            })
            .then((responseBody) => {
                setStarLinks(Object.values(responseBody._embedded)[0])
            })
            .catch((error) => {
                console.error(`Could not retrieve star links: ${error}`);
            })
        }
    }, [itemModel, isEditForm, setStarLinks])

    return (
        <>
            <OutletBasedFormDialog
                itemModelState={itemModelState}
                isEditFormState={isEditFormState}
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
                                        autoComplete: "off"
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
                        </Tab>
                        <Tab
                            eventKey="starLinks"
                            title="Star Links"
                        >
                            <StarLinksEditableList
                                starLinksState={starLinksState}
                                starLinksPendingRemovalState={starLinksPendingRemovalState}
                            />
                        </Tab>
                    </Tabs>
                }
            />
            
        </>
    );
}

export default OutletBasedStarFormDialog;