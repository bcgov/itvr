import TextField from '@mui/material/TextField';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { getFirstDayOfMonth, getLastDayOfMonth } from '../utility';

const DateBoxes = ({ maxDate, minDate, value, onChange }) => {
  return (
    <>
      <DatePicker
        maxDate={maxDate}
        minDate={minDate}
        label="Year"
        views={['year']}
        value={value}
        onChange={(newDate) => {
          onChange(newDate);
        }}
        renderInput={(params) => (
          <TextField
            id="year_of_birth"
            {...params}
            inputProps={{
              ...params.inputProps,
              readOnly: true
            }}
          />
        )}
      />
      <DatePicker
        maxDate={maxDate}
        minDate={minDate}
        label="Month"
        views={['month']}
        value={value}
        onChange={(newDate) => {
          onChange(newDate);
        }}
        renderInput={(params) => (
          <TextField
            id="month_of_birth"
            {...params}
            inputProps={{
              ...params.inputProps,
              readOnly: true,
              value:
                (value.getMonth() + 1).toString().padStart(2, '0') +
                ' - ' +
                value.toLocaleString('default', {
                  month: 'long'
                })
            }}
          />
        )}
      />
      <DatePicker
        maxDate={
          maxDate < getLastDayOfMonth(value)
            ? maxDate
            : getLastDayOfMonth(value)
        }
        minDate={
          getFirstDayOfMonth(value) < minDate
            ? minDate
            : getFirstDayOfMonth(value)
        }
        label="Day"
        views={['day']}
        value={value}
        onChange={(newDate) => {
          onChange(newDate);
        }}
        renderInput={(params) => (
          <TextField
            id="day_of_birth"
            {...params}
            inputProps={{
              ...params.inputProps,
              readOnly: true,
              value: value.getDate()
            }}
          />
        )}
      />
    </>
  );
};

export default DateBoxes;
