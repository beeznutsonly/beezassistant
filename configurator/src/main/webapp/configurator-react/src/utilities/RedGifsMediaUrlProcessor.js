import MediaObject from "../models/MediaObject";

class RedGifsMediaUrlProcessor {

    static HOST_NAME_MATCH = /(www\.)?redgifs.com/;
    static API_ADDRESS = "https://api.redgifs.com";
    static BEARER_TOKEN;

    static {
        fetch(
            `${this.API_ADDRESS}/v2/auth/temporary`,
            {
                headers: {"Content-Type":"application/json"}
            }
        ).then((response) => {
            if (response.ok) {
                return response.json()
            }
            else {
                return Promise.reject(response.status)
            }
        }).then((responseBody) => {
            this.BEARER_TOKEN = responseBody.token
        }).catch(error => {
            console.error(error);
        })
    }

    static processUrl(url, callback) {
        if (!Boolean(
            url.hostname.match(RedGifsMediaUrlProcessor.HOST_NAME_MATCH)
        )) {
            throw new Error(`Url hostname is invalid (${url.hostname})`)
        }
        
        const urlPathParts = url.pathname.split('/');
        fetch(
            `${RedGifsMediaUrlProcessor.API_ADDRESS}/v2/gifs/${urlPathParts[urlPathParts.length - 1]}`,
            {
                headers: {
                    "Content-Type":"application/json",
                    "Authorization": `Bearer ${RedGifsMediaUrlProcessor.BEARER_TOKEN}`
                }
            }
        ).then((response) => {
            if (response.ok) {
                return response.json()
            }
            else {
                return Promise.reject(response.status)
            }
        })
        .then((responseJson) => {
            if (responseJson.errorMessage) {
                callback(responseJson)
            }
            else {
                callback(new MediaObject(
                    responseJson.gif.tags.join(" "),
                    responseJson.gif.createDate,
                    responseJson.gif.userName,
                    responseJson.gif.urls.thumbnail
                ));
            }
        })
        .catch((error) => {
            console.error(error);
        });
    }

}

export default RedGifsMediaUrlProcessor;