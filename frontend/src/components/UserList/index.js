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
  BooleanInput,
  AutocompleteInput,
  usePermissions,
} from 'react-admin';

const UserListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/users');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export const UserCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="username" />
      <TextInput source="password" />
      <TextInput source="displayName" />
      <TextInput source="email" />
      <AutocompleteInput
        source="role"
        choices={[
          { id: 'admin', name: 'Администратор' },
          { id: 'sales_department', name: 'Отдел продаж' },
          { id: 'law_department', name: 'Юридический отдел' },
          { id: 'logistics_department', name: 'Отдел логистики' },
          { id: 'branches', name: 'Филиал' },
          { id: 'demo', name: 'Демо' },
        ]}
      />
    </SimpleForm>
  </Create>
);

export const UserEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput disabled source="username" />
      <TextInput source="displayName" />
      <TextInput source="password" />
      <BooleanInput source="deactivated" />
      <AutocompleteInput
        source="role"
        choices={[
          { id: 'admin', name: 'Администратор' },
          { id: 'sales_department', name: 'Отдел продаж' },
          { id: 'law_department', name: 'Юридический отдел' },
          { id: 'logistics_department', name: 'Отдел логистики' },
          { id: 'branches', name: 'Филиал' },
          { id: 'demo', name: 'Демо' },
        ]}
      />
    </SimpleForm>
  </Edit>
);

export const UserList = (props) => (
  <List {...props} actions={<UserListActions />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="displayName" />
      <TextField source="role" />
    </Datagrid>
  </List>
);

export default UserList;
