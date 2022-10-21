import DateAdapter from '@date-io/date-fns';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Accordion from 'react-bootstrap/Accordion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import "./Star.css";

const Star = (props) => {

    const dateAdapter = new DateAdapter();

    return (
        <>
            <div className="star general-list-group-item-content">
                <div className="star-core">
                    <div className="star-core-details">
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
                    <ButtonGroup className="secondary-details-button-group">
                        <button className="btn">
                        </button>
                        <button className="btn">
                    
                        </button>
                    </ButtonGroup>
                </div>
                {
                    Boolean(props.description)
                    ? (
                        <Accordion flush>
                            <Accordion.Item eventKey="0">
                                {/* <Accordion.Header>Description</Accordion.Header> */}
                                <Accordion.Body>
                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                        { props.description }
                                    </ReactMarkdown>
                                </Accordion.Body>
                            </Accordion.Item>
                        </Accordion>
                    )
                    : <></>
                }
            </div>
        </>
    );
}

export default Star;