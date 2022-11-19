import { useCallback, useState } from "react";
import AlertModel from "./AlertModel"

export default function useAlertModelAndController() {
    
    const [alertModel, setAlertModel] = useState(
        AlertModel.defaultModel()
    );

    const openAlert = useCallback((variant, body, heading = "") => {
        setAlertModel(
            new AlertModel(
                true,
                variant,
                body,
                heading
            )
        )
    }, []);

    const closeAlert = () => {
        setAlertModel(oldAlertModel => ({
            ...oldAlertModel, isShown: false
        }))
    };

    return {
        alertModel: alertModel,
        alertController: {
            openAlert: openAlert,
            closeAlert: closeAlert
        }
    }

}