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
  Filter,
  usePermissions,
  Show,
  SimpleShowLayout,
  EmailField,
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

const ProviderFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="name" alwaysOn />
  </Filter>
);

export const ProviderCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="name" />
      <TextInput source="email" />
      <TextInput source="phone" />
      <TextInput source="address" />
      <TextInput multiline source="data" />
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
        <TextInput
          multiline
          disabled={
            !permissions.actions.includes('update')
            && !permissions.actions.includes('update_status')
          }
          source="data"
        />
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

export const ProviderShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="phone" />
      <EmailField source="email" />
      <TextField source="address" />
      <TextField source="data" />
      <TextField source="status" />
    </SimpleShowLayout>
  </Show>
);

export const ProviderList = (props) => (
  <List
    {...props}
    actions={<ProviderListActions />}
    bulkActionButtons={false}
    filters={<ProviderFilter />}
  >
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="status" />
    </Datagrid>
  </List>
);

export default ProviderList;
