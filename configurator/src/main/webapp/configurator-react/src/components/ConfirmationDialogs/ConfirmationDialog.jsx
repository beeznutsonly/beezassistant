import Modal from 'react-bootstrap/Modal';

const ConfirmationDialog = (props) => {

    const [confirmationDialogModel, setConfirmationDialogModel] = props.confirmationDialogState;

    const closeDialog = () => {
        setConfirmationDialogModel({
            ...confirmationDialogModel,
            "isShown": false
        });
    }

    return (
        <>
            <Modal
                show={confirmationDialogModel.isShown}
                onHide={() => closeDialog()}
            >
                <Modal.Body>{confirmationDialogModel.body}</Modal.Body>
                <Modal.Footer>
                    <button 
                        className="btn btn-secondary" 
                        onClick={() => closeDialog()}
                    >
                        Cancel
                    </button>
                    <button 
                        className="btn btn-primary" 
                        onClick={() => {
                            closeDialog();
                            confirmationDialogModel.confirmedCallback();
                        }}
                    >
                        Confirm
                    </button>
                </Modal.Footer>
            </Modal>
        </>
    );
};

export default ConfirmationDialog;