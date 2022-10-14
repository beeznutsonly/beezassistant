import DateAdapter from '@date-io/date-fns';
import "./Star.css";

const Star = (props) => {

    const dateAdapter = new DateAdapter();

    return (
        <>
            <div className="star general-list-group-item-content">
                <h2 className="star-name">{props.name}</h2>
                <label className="star-birthday">{
                    Boolean(props.birthday)
                    ? dateAdapter.formatByString(dateAdapter.date(props.birthday), 'PP')
                    : props.birthday
                }</label>
                <label className="star-nationality">Nationality: {props.nationality}</label>
                <label className="star-birth-place">Birth Place: {props.birthPlace}</label>
                <label className="star-years-active">Years Active: {props.yearsActive}</label>
            </div>
        </>
    );
}

export default Star;