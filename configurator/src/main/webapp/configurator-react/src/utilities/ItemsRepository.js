class ItemsRepository {

    constructor(repositoryURL){
        this.repositoryURL = repositoryURL;
    }

    addItem(item) {
        return fetch(
            this.repositoryURL,
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(item)
            }
        );
    }

    updateItem(item) {
        return fetch(
            item._links.self.href,
            {
                method: "PATCH",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(item)
            }
        );
    }

    removeItem(item) {
        return fetch(
            item._links.self.href,
            {
                method: "DELETE",
                headers: {"Content-Type":"application/json"}
            }
        );
    }

    retrieveItems() {
        return fetch(this.repositoryURL, {
            headers: {"Content-Type":"application/json"}
        });
    }

    retrieveItem(itemId) {
        return fetch(`${this.repositoryURL}/${itemId}`, {
            headers: {"Content-Type":"application/json"}
        });
    }

    static getItemId(item) {
        const pathNameSegments = new URL(
            item._links.self.href
        ).pathname.split('/'); 
        return pathNameSegments[pathNameSegments.length - 1];
    }
}

export default ItemsRepository;