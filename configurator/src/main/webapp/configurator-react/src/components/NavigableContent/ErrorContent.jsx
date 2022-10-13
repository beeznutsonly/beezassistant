import ContentShard from "../ContentShards/StandardContentShard";

const ErrorContent = () => {
    return (
        <>
            <ContentShard title="Page Not Found">
                <p>Unfortunately, we could not find your page</p>
            </ContentShard>
        </>
    );
}

export default ErrorContent;