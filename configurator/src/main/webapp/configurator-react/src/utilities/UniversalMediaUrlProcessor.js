class UniversalMediaUrlProcessor {

    constructor(mediaUrlProcessorMap) {
        this.mediaUrlProcessorMap = mediaUrlProcessorMap;
    }

    processUrl(urlString, callback) {
        const url = new URL(urlString);

        if (this.mediaUrlProcessorMap[url.hostname]) {
            this.mediaUrlProcessorMap[
                url.hostname
            ].processUrl(url, callback)
        }
    }
    
}

export default UniversalMediaUrlProcessor;