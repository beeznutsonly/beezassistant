import { useCallback, useEffect } from 'react';
import { useLocation, useOutletContext, useParams } from 'react-router-dom';
import ItemDialogForm from '../Forms/ItemDialogForm';
import BasicFormDialog from './BasicFormDialog';

const OutletBasedFormDialog = (props) => {
    
    const [itemModel, setItemModel] = props.itemModelState;
    const context = useOutletContext();
    const location = useLocation();
    const params = useParams();
    const [isEditForm, setIsEditForm] = props.isEditFormState;

    const submitSuccessHandler = useCallback((item) => {
        if (isEditForm) {
            context.editItemTools.submitSuccessCallback(item);
        }
        else {
            context.addItemTools.submitSuccessCallback(item);
        }
    }, [
        isEditForm,
        context.addItemTools,
        context.editItemTools
    ])

    const retrieveItemModel = useCallback(() => {
        if (location.state) {
            setItemModel(location.state);
        }
        else {
            if (params["itemId"]) {
                const promise = context.itemsAPI.retrieveItem(
                    encodeURI(`${params["itemId"]}`)
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
        context.itemsAPI,
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
                        secondarySuccessCallback={context.secondarySuccessCallback}
                        isActionInProgressState={
                            isEditForm
                            ? context.editItemTools.isActionInProgressState
                            : context.addItemTools.isActionInProgressState
                        }
                        itemAPIAction={(item) => isEditForm 
                            ? context.itemsAPI.updateItem(item)
                            : context.itemsAPI.addItem(item)
                        }
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