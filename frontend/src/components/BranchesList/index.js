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
  Filter,
  usePermissions,
  Show,
  SimpleShowLayout,
  ReferenceArrayField,
} from 'react-admin';

const BranchListActions = () => {
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

const BranchFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="address" alwaysOn />
  </Filter>
);

export const BranchCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="address" />
    </SimpleForm>
  </Create>
);

export const BranchEdit = (props) => (
  <Edit undoable={false} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="address" />
    </SimpleForm>
  </Edit>
);

export const BranchShow = (props) => (
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

export const BranchesList = (props) => (
  <List
    {...props}
    actions={<BranchListActions />}
    bulkActionButtons={false}
    filters={<BranchFilter />}
  >
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="address" />
    </Datagrid>
  </List>
);

export default BranchesList;
