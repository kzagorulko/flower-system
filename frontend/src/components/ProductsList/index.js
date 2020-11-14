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
  ImageField,
  ImageInput,
  Filter,
  usePermissions,
} from 'react-admin';

const ProductListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/products');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const ProductFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="name" alwaysOn />
  </Filter>
);

export const ProductCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <ImageInput source="image" title="image">
        <ImageField source="image_path" title="image" />
      </ImageInput>
      <TextInput source="name" />
      <TextInput source="price" />
      <TextInput source="description" multiline />
    </SimpleForm>
  </Create>
);

export const ProductEdit = (props) => {
  const { loaded } = usePermissions('/products');

  return loaded ? (
    <Edit undoable={false} {...props}>
      <SimpleForm>
        <TextInput disabled source="id" />
        <ImageInput source="image" title="image">
          <ImageField source="image_path" title="image" />
        </ImageInput>
        <TextInput source="name" />
        <TextInput source="price" />
        <TextInput source="description" multiline />
      </SimpleForm>
    </Edit>
  ) : null;
};

export const ProductList = (props) => (
  <List {...props} actions={<ProductListActions />} filters={<ProductFilter />}>
    <Datagrid rowClick="edit">
      <ImageField source="image_path" title="image" sortable={false} />
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="price" />
    </Datagrid>
  </List>
);

export default ProductList;
