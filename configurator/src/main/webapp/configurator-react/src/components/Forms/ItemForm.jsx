import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import "./BasicForm.css";
import LoadingAnimationModel from '../../models/InlineLoadingAnimationModel';
import LoadingAnimation from '../LoadingAnimations/BasicInlineLoadingAnimation';
import useAlertModelAndController from '../Alerts/useAlertModelAndController';
import BasicAlert from '../Alerts/BasicAlert';

const ItemForm = ({
    formTitle,
    itemModel,
    isActionInProgressState,
    itemRepositoryAction,
    successMessage,
    failureMessage,
    submitSuccessHandler,
    children
}) => {

    const { alertModel, alertController } = useAlertModelAndController();
    const [isFormValidated, setFormValidated] = useState(false);
    const [isActionInProgress, setIsActionInProgress] = isActionInProgressState;

    const submitForm = () => {
        setIsActionInProgress(true);
        const promise = itemRepositoryAction(itemModel);
        promise.then((response) => {
            if (response.ok) {
                return response.json();
            }
            else {
                return Promise.reject(new Error(response.status));
            }
        })
        .then((item) => {
            alertController.openAlert(
                "success",
                successMessage
            )
            if (submitSuccessHandler) {
                submitSuccessHandler(item);
            }
        })
        .catch((error) => alertController.openAlert(
            "danger",
            `${failureMessage}: ${error.message}`
        ))
        .finally(() => {
            setIsActionInProgress(false);
        });
    }

    const handleSubmitForm = (event) => {
        if (event.currentTarget.checkValidity() === true){
            setFormValidated(true);
            event.preventDefault();
            event.stopPropagation();
            alertController.closeAlert();
            submitForm();
        }
        else {
            event.preventDefault();
            event.stopPropagation();
            setFormValidated(true);
        }
    }

    return (
        <>
            <Form 
                className="form-pane-standard v-flexbox" 
                onSubmit={handleSubmitForm}
                validated={isFormValidated} 
                noValidate
            >
                {
                    Boolean(formTitle)
                    ? (
                        <div className="form-heading">
                            <h1 className="form-title">{formTitle}</h1>
                        </div>
                    )
                    : <></>
                }
                <div className="form-content">
                    {children}
                </div>
                <BasicAlert 
                    alertModel={alertModel}
                    alertController={alertController}
                />
                <button 
                    className="btn btn-outline-primary" 
                    type="submit"
                    disabled={isActionInProgress}
                >
                    {
                        isActionInProgress 
                        ? <LoadingAnimation 
                            loadingAnimationModel={
                                LoadingAnimationModel.defaultLoadingAnimationModel()
                            } 
                        /> 
                        : "Submit"
                    }
                </button>
            </Form>
        </>
    );
}

export default ItemForm;