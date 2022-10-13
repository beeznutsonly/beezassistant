import Spinner from "react-bootstrap/Spinner";
import "./BasicInlineLoadingAnimation.css";

const BasicInlineLoadingAnimation = (props) => {
    
    return props.loadingAnimationModel.isShown 
            ? <Spinner 
                className="loading-animation inline-loading-animation"
                animation={props.loadingAnimationModel.animation}
                size={props.loadingAnimationModel.size} 
              />
            : <></> 
}

export default BasicInlineLoadingAnimation;