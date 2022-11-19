import Alert from 'react-bootstrap/Alert';
import './BasicAlert.css';

const BasicAlert = ({
    alertModel, 
    alertController
}) => {

    return (
        <div className="alert-card">
            <Alert
                show={alertModel.isShown}
                variant={alertModel.variant}
                onClose={() => alertController.closeAlert()}
            >
                {alertModel.heading
                    ? <><Alert.Heading>{alertModel.heading}</Alert.Heading><hr/></>
                    : <></>
                }
                {alertModel.body}
            </Alert>
        </div>
    );
}

export default BasicAlert;