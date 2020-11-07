/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  useListContext,
  CreateButton,
  TopToolbar,
  SimpleForm,
  Create,
  Edit,
  TextInput,
  AutocompleteInput,
  usePermissions,
} from 'react-admin';

const ProviderListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/providers');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export const ProviderCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="name" />
      <TextInput source="email" />
      <TextInput source="phone" />
      <TextInput source="address" />
      <TextInput source="data" />
    </SimpleForm>
  </Create>
);

export const ProviderEdit = (props) => {
  const { loaded, permissions } = usePermissions('/providers');

  return loaded ? (
    <Edit undoable={false} {...props}>
      <SimpleForm>
        <TextInput disabled source="id" />
        <TextInput disabled={!permissions.actions.includes('update')} source="name" />
        <TextInput disabled={!permissions.actions.includes('update')} source="email" />
        <TextInput disabled={!permissions.actions.includes('update')} source="phone" />
        <TextInput disabled={!permissions.actions.includes('update')} source="address" />
        <TextInput disabled={!permissions.actions.includes('update')} source="data" />
        <AutocompleteInput
          source="status"
          disabled={!permissions.actions.includes('update_status')}
          choices={[
            { id: 'new', name: 'New' },
            { id: 'cooperate', name: 'Cooperate' },
            { id: 'fraud', name: 'Fraud' },
            { id: 'stopped', name: 'Stopped' },
          ]}
        />
      </SimpleForm>
    </Edit>
  ) : null;
};

export const ProviderList = (props) => (
  <List {...props} actions={<ProviderListActions />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="status" />
    </Datagrid>
  </List>
);

export default ProviderList;
