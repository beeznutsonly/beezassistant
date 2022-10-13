import { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import { useNavigate } from 'react-router-dom';
import "./BasicFormDialog.css";

const BasicFormDialog = (props) => {

    const [isModalShown, setModalShown] = useState(true);
    const navigate = useNavigate();

    const closeDialog = () => {
        setModalShown(false);
    }

    return (
        <>
            <Modal
                className="form-dialog"
                show={isModalShown}
                onHide={() => closeDialog()}
                onExited={() => navigate("..", { replace: true } )}
            >
                <Modal.Header closeButton></Modal.Header>
                <Modal.Body>
                    {props.form}
                </Modal.Body>
            </Modal>
        </>
    );
}

export default BasicFormDialog;