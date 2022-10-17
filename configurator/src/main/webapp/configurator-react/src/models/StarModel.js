class StarModel {

    constructor (
        name,
        birthday,
        nationality,
        birthPlace,
        yearsActive,
        description
    ) {
        this.name = name;
        this.birthday = birthday;
        this.nationality = nationality;
        this.birthPlace = birthPlace;
        this.yearsActive = yearsActive;
        this.description = description;
    }

    static defaultItemModel() {
        return new StarModel(
            "", "", "", null, "", ""
        );
    }
}

export default StarModel;