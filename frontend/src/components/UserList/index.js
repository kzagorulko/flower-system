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
} from 'react-admin';

const UserListActions = () => {
  const {
    basePath,
  } = useListContext();

  return (
    <TopToolbar>
      <CreateButton basePath={basePath} />
    </TopToolbar>
  );
};

export const UserCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="username" />
      <TextInput source="password" />
      <TextInput source="displayName" />
      <TextInput source="email" />
      <TextInput source="role" />
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
      <TextInput source="role" />
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
