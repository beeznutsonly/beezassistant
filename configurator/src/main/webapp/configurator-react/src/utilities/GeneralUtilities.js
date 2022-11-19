
const delay = (duration, callBack = () => { }) => {
    setTimeout(callBack, duration);
}

export { delay };