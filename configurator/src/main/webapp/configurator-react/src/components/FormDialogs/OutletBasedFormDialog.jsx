import { useCallback, useEffect } from 'react';
import { useLocation, useOutletContext, useParams } from 'react-router-dom';
import ItemDialogForm from '../Forms/ItemDialogForm';
import BasicFormDialog from './BasicFormDialog';

const OutletBasedFormDialog = (props) => {
    
    const [itemModel, setItemModel] = props.itemModelState;
    const itemManipulationTools = useOutletContext();
    const location = useLocation();
    const params = useParams();
    const [isEditForm, setIsEditForm] = props.isEditFormState;

    const submitSuccessHandler = useCallback((item) => {
        if (isEditForm) {
            itemManipulationTools.editItemTools.submitSuccessCallback(item);
        }
        else {
            itemManipulationTools.addItemTools.submitSuccessCallback(item);
        }
    }, [
        isEditForm,
        itemManipulationTools.addItemTools,
        itemManipulationTools.editItemTools
    ])

    const retrieveItemModel = useCallback(() => {
        if (location.state) {
            setItemModel(location.state);
        }
        else {
            if (params["itemId"]) {
                const promise = itemManipulationTools.itemsAPI.retrieveItem(
                    encodeURI(params["itemId"])
                );
                promise.then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    else {
                        return Promise.reject(new Error(response.status));
                    }
                })
                .then((item) => {
                    setItemModel(item);
                })
                .catch((error) => {
                    console.error(`Could not retrieve item model: ${error}`);
                    if (isEditForm) setIsEditForm(false);
                });
            }
        }
    }, [
        location.state,
        isEditForm,
        setIsEditForm,
        itemManipulationTools.itemsAPI,
        setItemModel,
        params
    ])

    useEffect(() => {
        retrieveItemModel();
    }, [retrieveItemModel])
    

    return (
        <>
            <BasicFormDialog 
                form={
                    <ItemDialogForm
                        formTitle={props.formTitle}
                        itemModel={itemModel}
                        submitSuccessHandler={submitSuccessHandler}
                        isActionInProgressState={
                            isEditForm
                            ? itemManipulationTools.editItemTools.isActionInProgressState
                            : itemManipulationTools.addItemTools.isActionInProgressState
                        }
                        itemAPIAction={(item) => itemManipulationTools.itemsAPI.addItem(item)}
                        successMessage={
                            `Item successfully ${isEditForm ? "modified" : "added"}`
                        }
                        failureMessage={
                            `Failed to ${isEditForm ? "edit" : "add"} item`
                        }                
                    >
                        {props.itemFormContent}
                    </ItemDialogForm>
                }
            />
        </>
    );

}

export default OutletBasedFormDialog;