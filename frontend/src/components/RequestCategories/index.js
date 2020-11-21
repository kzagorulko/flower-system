import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  SimpleForm,
  Create,
  TextInput,
  Show,
  SimpleShowLayout,
  Edit,
  SaveButton,
  Toolbar,
} from 'react-admin';

const CustomToolbar = (props) => (
  <Toolbar {...props}>
    <SaveButton />
  </Toolbar>
);

export const RequestCategoryList = (props) => (
  <List {...props}>
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="name" />
    </Datagrid>
  </List>
);

export const RequestCategoryCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="name" />
    </SimpleForm>
  </Create>
);

export const RequestCategoryShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="name" />
    </SimpleShowLayout>
  </Show>
);

export const RequestCategoryEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm toolbar={<CustomToolbar />}>
      <TextInput source="name" />
    </SimpleForm>
  </Edit>
);
