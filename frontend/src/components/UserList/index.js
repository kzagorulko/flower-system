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
  SimpleShowLayout,
  BooleanField,
  TextInput,
  BooleanInput,
  AutocompleteInput,
  Filter,
  usePermissions,
  ReferenceInput,
  ReferenceField,
  SelectInput,
} from 'react-admin';

const rolesChoices = [
  { id: 'admin', name: 'Администрация' },
  { id: 'sales_department', name: 'Отдел продаж' },
  { id: 'law_department', name: 'Юридический отдел' },
  { id: 'logistics_department', name: 'Отдел логистики' },
  { id: 'branches', name: 'Филиал' },
  { id: 'demo', name: 'Демо' },
];

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

const UserFilter = (props) => (
  <Filter {...props}>
    <TextInput label="Search" source="display_name" alwaysOn />
    <SelectInput label="Роли" source="role" choices={rolesChoices} alwaysOn />
  </Filter>
);

export const UserCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="username" />
      <TextInput source="password" />
      <TextInput source="displayName" />
      <TextInput source="email" />
      <AutocompleteInput
        source="role"
        choices={rolesChoices}
        optionValue="name"
      />
      <ReferenceInput label="Branches" source="branch_id" reference="branches">
        <AutocompleteInput optionText="address" optionValue="id" allowEmpty />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
export const UserShow = (props) => (
  <Show title="Showing User" {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="username" />
      <TextField source="displayName" />
      <BooleanField source="deactivated" />
      <TextField source="email" />
      <ReferenceField label="Branches" source="branch_id" reference="branches">
        <TextField source="address" />
      </ReferenceField>
    </SimpleShowLayout>
  </Show>
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
        choices={rolesChoices}
        optionValue="name"
      />
      <ReferenceInput label="Branches" source="branch_id" reference="branches">
        <AutocompleteInput optionText="address" optionValue="id" allowEmpty />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);
export const UserList = (props) => (
  <List {...props} actions={<UserListActions />} filters={<UserFilter />}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="displayName" />
      <TextField source="role" />
    </Datagrid>
  </List>
);

export default UserList;
