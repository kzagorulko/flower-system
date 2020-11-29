import React from 'react';

import {
  List,
  Datagrid,
  TextField,
} from 'react-admin';

export const ContractList = (props) => {
  const { loading } = props || { loading: false };
  return !loading ? (
    <List {...props}>
      <Datagrid rowClick="show">
        <TextField source="id" />
      </Datagrid>
    </List>
  ) : null;
};

export const ContractShow = () => {};
