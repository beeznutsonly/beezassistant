import { getValidFormValue, isEditForm as isEditFormFunction, updateField } from '../../utilities/FormManipulationUtilities';
import OutletBasedFormDialog from './OutletBasedFormDialog';
import Form from 'react-bootstrap/Form';
import ItemModel from '../../models/StarModel';
import { useEffect, useState } from 'react';
import { useLocation, useOutletContext, useParams } from 'react-router-dom';
import DateTimePickerField from '../Forms/FormFieldControls/DateTimePickerField';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import ItemsRepository from '../../utilities/ItemsRepository';
import StarLinksEditableList from './StarLinksEditableList';
import './OutletBasedStarFormDialog.css';

const OutletBasedStarFormDialog = () => {

    const itemModelState = useState(ItemModel.defaultItemModel());
    const itemModel = itemModelState[0];
    const [isEditForm, setEditForm] = useState(
        isEditFormFunction(useLocation(), useParams())
    );

    // const [starLinksRepository, setStarLinksRepository] = useState();

    // const retrieveStarLinks = useCallback(() => {
    //     starLinksRepository.retrieveItems()
    //     .then((response) => {
    //         if (response.ok) {
    //             return response.json();
    //         }
    //         return Promise.reject(new Error(response.status));
    //     })
    //     .then((responseBody) => {
    //         setStarLinks(Object.values(responseBody._embedded)[0]);
    //     })
    //     .catch((error) => {
    //         console.error(`Could not retrieve star links: ${error}`);
    //     });
    // }, [starLinksRepository]);

    // const starSubmitSuccessCallback = (star) => {
    //     const starStarLinksRepository = new ItemsRepository(
    //         star._links.starLinks.href
    //     )
    //     if (isEditForm) {
    //         starLinksPendingRemoval.forEach(
    //             starLinkPendingRemoval => {
    //                 if (starLinkPendingRemoval._links)
    //                     starStarLinksRepository.removeItem(
    //                         starLinkPendingRemoval
    //                     )
    //                     .catch((error) => {
    //                         return Promise.reject(new Error(error))
    //                     })
    //             }
    //         )
    //         setStarLinksPendingRemoval(
    //             new Set()
    //         );
    //     }
    //     starLinks.forEach(
    //         starLink => starStarLinksRepository.addItem(
    //             starLink
    //         )
    //         .catch((error) => {
    //             return Promise.reject(new Error(error))
    //         })
    //     )
    // }

    // useOutletContext().secondarySuccessCallback = starSubmitSuccessCallback;

    // useEffect(() => {
    //     if (
    //         !(starLinks.length || starLinksPendingRemoval.size) 
    //         && Boolean(itemModel.starLinks)
    //     ) {
    //         setStarLinks(itemModel.starLinks)
    //     }
    // }, [starLinks, starLinksPendingRemoval, itemModel]);

    // useEffect(() => {
    //     if (isEditForm && starLinksRepository) {
    //         retrieveStarLinks()
    //     }
    // }, [
    //     isEditForm, 
    //     starLinksRepository, 
    //     retrieveStarLinks
    // ]);

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
                                // starLinksState={[starLinks, setStarLinks]}
                                // starLinksPendingRemovalState={
                                //     [starLinksPendingRemoval, setStarLinksPendingRemoval]
                                // }
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