const sortByStrings = (itemPropertyName, items, isSortAscend) =>
    [...items].sort((item1, item2) => {
        const inverter = isSortAscend ? 1 : -1;
        const string1 = item1[itemPropertyName];
        const string2 = item2[itemPropertyName];
        return string1.localeCompare(string2) * inverter;
    }
);

const sortByTime = (itemPropertyName, items, isSortAscend) =>
    [...items].sort((item1, item2) => {
        const inverter = isSortAscend ? 1 : -1;
        const item1Time = new Date(item1[itemPropertyName]);
        const item2Time = new Date(item2[itemPropertyName]);
        if (item1Time < item2Time) return -1 * inverter;
        if (item1Time > item2Time) return 1 * inverter;
        return 0;
    }
);

export {sortByStrings, sortByTime};