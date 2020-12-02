import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  NumberField,
  NumberInput,
  useListContext,
  CreateButton,
  TopToolbar,
  SimpleForm,
  Create,
  Edit,
  TextInput,
  Filter,
  usePermissions,
  Show,
  SimpleShowLayout,
  ArrayField,
} from 'react-admin';

const WarehouseListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/warehouses');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const WarehouseFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="address" alwaysOn />
  </Filter>
);

export const WarehouseCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="address" />
      <NumberInput source="max_value" />
    </SimpleForm>
  </Create>
);

export const WarehouseEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="address" />
      <NumberInput source="max_value" />
    </SimpleForm>
  </Edit>
);

export const WarehouseShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="address" />
      <NumberField source="max_value" />
      <NumberField source="left_amount" />
      <ArrayField source="products">
        <Datagrid>
          <TextField source="id" />
          <TextField source="value" />
        </Datagrid>
      </ArrayField>
    </SimpleShowLayout>
  </Show>
);

export const WarehouseList = (props) => (
  <List {...props} actions={<WarehouseListActions />} filters={<WarehouseFilter />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="address" />
      <NumberField source="max_value" />
      <NumberField source="left_amount" />
    </Datagrid>
  </List>
);

export default WarehouseList;
