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
  TextInput,
  Filter,
  usePermissions,
  Show,
  SimpleShowLayout,
  ReferenceArrayField,
  ReferenceField,
  DateField,
} from 'react-admin';

const PurchasesListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/branches');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const PurchaseFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="address" alwaysOn />
  </Filter>
);

export const PurchaseCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="address" />
    </SimpleForm>
  </Create>
);

export const PurchaseShow = (props) => (
  <Show {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="address" />
      <ReferenceArrayField label="Users" reference="users" source="user_ids">
        <Datagrid>
          <TextField source="id" />
          <TextField source="displayName" label="Name" />
        </Datagrid>
      </ReferenceArrayField>
    </SimpleShowLayout>
  </Show>
);

export const PurchasesList = (props) => (
  <List
    {...props}
    actions={<PurchasesListActions />}
    bulkActionButtons={false}
    filters={<PurchaseFilter />}
  >
    {/* search by product_id, warehouse_id, branch_id, startendDate */}
    <Datagrid rowClick="show">
      <TextField source="id" />
      <DateField source="date" showTime />
      <ReferenceField link="show" label="Product" source="product_id" reference="products">
        <TextField source="name" />
      </ReferenceField>
      <ReferenceField link="show" label="Warehouse" source="warehouse_id" reference="warehouses">
        <TextField source="address" />
      </ReferenceField>
      {/* to omit for branch users when backend branch filtering added */}
      <TextField source="address" label="Provider" />
      <TextField source="value" />
      <TextField source="status" />
    </Datagrid>
  </List>
);

export default PurchasesList;
