import React from 'react';

import {
  List,
  Datagrid,
  TextField,
  DateField,
  Show,
  SimpleShowLayout,
  ReferenceField,
  FileField,
} from 'react-admin';

export const ContractList = (props) => {
  const { loading } = props || { loading: false };
  return !loading ? (
    <List {...props}>
      <Datagrid rowClick="show">
        <TextField source="id" />
        <TextField source="number" />
        <TextField source="status" />
        <DateField source="startDate" />
        <DateField source="endDate" />
      </Datagrid>
    </List>
  ) : null;
};

export const ContractShow = (props) => {
  // const { loading } = props || { loading: false };
  console.log(props);
  return (
    <Show {...props}>
      <SimpleShowLayout>
        <TextField source="number" />
        <TextField source="status" />
        <DateField source="startDate" />
        <DateField source="endDate" />
        <ReferenceField label="Поставщик" source="providerId" reference="providers">
          <TextField source="name" />
        </ReferenceField>
        <FileField source="path" download title="Файл контракта" target="_blank" />
      </SimpleShowLayout>
    </Show>
  );
};
