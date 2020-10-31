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
    </SimpleForm>
  </Create>
);

export const UserEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="username" />
    </SimpleForm>
  </Edit>
);

export const UserList = (props) => (
  <List {...props} actions={<UserListActions />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="username" />
    </Datagrid>
  </List>
);

export default UserList;
