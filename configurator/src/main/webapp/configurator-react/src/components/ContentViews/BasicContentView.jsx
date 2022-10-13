import { Outlet } from "react-router-dom";
import "./ContentView.css"

const BasicContentView = () => {
    return(
        <>
            <main className="content-view">
                <Outlet />
            </main>
        </>
    );
}

export default BasicContentView;