import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import AlertModel from '../../models/AlertModel';
import "./DialogForm.css";
import LoadingAnimationModel from '../../models/InlineLoadingAnimationModel';
import LoadingAnimation from '../LoadingAnimations/BasicInlineLoadingAnimation';

const ItemDialogForm = (props) => {

    const [alertModel, setAlertModel] = useState(AlertModel.defaultAlertModel());
    const [isFormValidated, setFormValidated] = useState(false);
    const [isActionInProgress, setIsActionInProgress] = props.isActionInProgressState;

    const closeAlert = () => {
        setAlertModel({
            ...alertModel,
            isShown: false
        })
    }

    const openAlert = (body, variant) => {
        setAlertModel(
            new AlertModel(
                true,
                variant,
                "",
                body
            )
        )
    }

    const submitForm = () => {
        setIsActionInProgress(true);
        const promise = props.itemAPIAction(props.itemModel);
        promise.then((response) => {
            if (response.ok) {
                return response.json();
            }
            else {
                return Promise.reject(new Error(response.status));
            }
        })
        .then((responseBody) => {
            openAlert(
                props.successMessage,
                "success"
            )
            if (props.submitSuccessHandler) {
                props.submitSuccessHandler(responseBody);
            }
        })
        .catch((error) => openAlert(
            `${props.failureMessage}: ${error.message}`
            , "danger"
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
            closeAlert();
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
                <div className="form-heading v-flexbox">
                    <h1 className="form-title">{props.formTitle}</h1>
                </div>
                <div className="form-content">
                    {props.children}
                </div>
                <div className="feedback-alert-card">
                    <Alert
                        show={alertModel.isShown && !isActionInProgress}
                        variant={alertModel.variant}
                        onClose={() => closeAlert()}
                    >
                        {alertModel.body}
                    </Alert>
                </div>
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

export default ItemDialogForm;