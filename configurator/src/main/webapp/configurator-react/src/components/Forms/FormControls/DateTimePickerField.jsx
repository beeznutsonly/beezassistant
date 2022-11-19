import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { useState } from "react";
import { Form } from "react-bootstrap";


const DateTimePickerField = ({
    formItemModelState,
    dateTimeFieldName,
    inputProps,
    isDateOnly,
    inputFormat,
    minDateTime
}) => {

    const [isOpen, setOpen] = useState(false);
    const [formItemModel, setFormItemModel] = formItemModelState;

    return (
        <>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DateTimePicker 
                    open={isOpen}
                    onClose={() => setOpen(false)}
                    renderInput={(defaultInputProps) => 
                        <Form.Control
                            {...defaultInputProps.inputProps}
                            {...inputProps}
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
                        isDateOnly 
                        ? ['year', 'month', 'day'] 
                        : ['year', 'day', 'hours', 'minutes']
                    }
                    ampm={false}
                    disableMaskedInput
                    inputFormat={inputFormat}
                    minDateTime={minDateTime}
                />
            </LocalizationProvider>
        </>
    );
}

export default DateTimePickerField;