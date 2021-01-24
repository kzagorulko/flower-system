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
  Create,
  SimpleForm,
  TextInput,
  DateInput,
  ReferenceInput,
  AutocompleteInput,
  FileInput,
  required,
  Edit,
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

export const ContractShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="number" />
      <TextField source="status" />
      <TextField source="cancelDescription" />
      <DateField source="startDate" />
      <DateField source="endDate" />
      <ReferenceField label="Поставщик" source="providerId" reference="providers">
        <TextField source="name" />
      </ReferenceField>
      <FileField source="path" download title="Файл контракта" target="_blank" />
    </SimpleShowLayout>
  </Show>
);

export const ContractCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="number" validate={required()} />
      <DateInput source="startDate" validate={required()} />
      <DateInput source="endDate" validate={required()} />
      <ReferenceInput reference="providers" source="providerId" validate={required()}>
        <AutocompleteInput optionText="name" optionValue="id" allowEmpty />
      </ReferenceInput>
      <FileInput source="file" validate={required()}>
        <FileField source="file" title="Файл контракта" target="_blank" />
      </FileInput>
    </SimpleForm>
  </Create>
);

export const ContractEdit = (props) => (
  <Edit undoable={false} title="Отмена контракта" {...props}>
    <SimpleForm>
      <TextInput multiline source="cancelDescription" label="Причина отмены контракта" />
    </SimpleForm>
  </Edit>
);
