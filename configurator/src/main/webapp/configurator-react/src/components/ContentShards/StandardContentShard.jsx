import { useLayoutEffect } from "react";
import BasicAlert from "../Alerts/BasicAlert";
import BasicInlineLoadingAnimation from "../LoadingAnimations/BasicInlineLoadingAnimation";
import "./StandardContentShard.css";

const StandardContentShard = ({
    title,
    alertModelAndController,
    loadingAnimationModel,
    children
}) => {

    useLayoutEffect(() => {
        document.title = title;
    }, [title]);

    return (
        <div className="content-shard-container dynamic-shard">
            <div className="standard-content-shard">
                <header className="shard-heading">
                    <div className="shard-title-container">
                        <h1 className="shard-title">{title}</h1>
                        {
                            loadingAnimationModel && (
                                <BasicInlineLoadingAnimation
                                    loadingAnimationModel={loadingAnimationModel}
                                />
                            )

                        }
                    </div>
                    <hr/>
                </header>
                {
                    alertModelAndController && (
                        <BasicAlert 
                            alertModel={alertModelAndController.alertModel} 
                            alertController={alertModelAndController.alertController}
                        />
                    )
                }
                <div className="shard-content">{children}</div>
            </div>
        </div>
    )
}

export default StandardContentShard;