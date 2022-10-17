import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { useState } from "react";
import { Form } from "react-bootstrap";


const DateTimePickerField = (props) => {

    const [isOpen, setOpen] = useState(false);
    const [formItemModel, setFormItemModel] = props.formItemModelState;
    const dateTimeFieldName = props.dateTimeFieldName;

    return (
        <>
            <DateTimePicker 
                open={isOpen}
                onClose={() => setOpen(false)}
                renderInput={(defaultInputProps) => 
                    <Form.Control
                        {...defaultInputProps.inputProps}
                        {...props.inputProps}
                        onClick={() => setOpen(true)}
                        type={defaultInputProps.inputProps.type}
                        ref={defaultInputProps.inputRef}
                    >
                    </Form.Control>
                }
                value={formItemModel[dateTimeFieldName]}
                onChange={(newValue) => {
                    formItemModel[dateTimeFieldName] = newValue
                    setFormItemModel({...formItemModel});
                }}
                views={
                    props.isDateOnly 
                    ? ['year', 'month', 'day'] 
                    : ['year', 'day', 'hours', 'minutes']
                }
                ampm={false}
                inputFormat={props.inputFormat}
                minDateTime={props.minDateTime}
            />
        </>
    );
}

export default DateTimePickerField;