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
  Show,
  TextInput,
  ImageField,
  ImageInput,
  Filter,
  usePermissions,
  SimpleShowLayout,
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

export const ProductEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <ImageInput source="file" title="image">
        <ImageField source="file_path" title="image" />
      </ImageInput>
      <TextInput source="name" />
      <TextInput source="price" />
      <TextInput source="description" multiline />
    </SimpleForm>
  </Edit>
);

export const ProductShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <ImageField source="image_path" title="image" />
      <TextField source="name" />
      <TextField source="price" />
      <TextField source="description" />
    </SimpleShowLayout>
  </Show>
);

export const ProductList = (props) => (
  <List
    {...props}
    actions={<ProductListActions />}
    bulkActionButtons={false}
    filters={<ProductFilter />}
  >
    <Datagrid rowClick="edit">
      <ImageField source="image_path" title="image" sortable={false} />
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="price" />
    </Datagrid>
  </List>
);

export default ProductList;
