import { useLayoutEffect } from "react";
import "./StandardContentShard.css";

const StandardContentShard = (props) => {

    useLayoutEffect(() => {
      document.title = props.title;
    }, [props.title]);

    return (
        <div className="content-shard-container dynamic-shard">
            <div className="standard-content-shard">
                <header className="shard-heading">
                    <div className="shard-title-container">
                        <h1 className="shard-title">{props.title}</h1>
                        {props.loadingAnimation}
                    </div>
                    <hr/>
                </header>
                {props.alertContainer ? props.alertContainer : <></>}
                <div className="shard-content">{props.children}</div>
            </div>
        </div>
    )
}

export default StandardContentShard;