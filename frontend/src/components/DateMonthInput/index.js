/* eslint-disable react/destructuring-assignment */
import React from 'react';
import TextField from '@material-ui/core/TextField';
import { useInput } from 'react-admin';

const DateMonthInput = (props) => {
  const {
    input: {
      name,
      onChange,
      value,
      ...rest
    },
    meta: { touched, error },
  } = useInput(props);
  const { label } = props;

  const date = new Date();
  const month = `${date.getMonth() + 1}`.padStart(0, 2);
  const year = date.getFullYear();
  const currentMonthControl = `${year}-${month}`;

  return (
    <TextField
      name={name}
      label={label}
      type="month"
      onChange={onChange}
      value={value || currentMonthControl}
      error={!!(touched && error)}
      helperText={touched && error}
      margin="normal"
      {...rest}
    />
  );
};

export default DateMonthInput;
