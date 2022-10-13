import Alert from 'react-bootstrap/Alert';

const AlertContainer = (props) => {
    const [alertModel, setAlertModel] = props.alertState;

    const closeAlert = () => {
        setAlertModel({
            ...alertModel,
            "isShown": false
        })
    }

    return (
        <div className="feedback-alert-card">
            <Alert
                show={alertModel.isShown}
                variant={alertModel.variant}
                onClose={() => closeAlert()}
            >
                {alertModel.heading
                    ? <><Alert.Heading>{alertModel.heading}</Alert.Heading><hr/></>
                    : <></>
                }
                {alertModel.body}
            </Alert>
        </div>
    );
};

export default AlertContainer;