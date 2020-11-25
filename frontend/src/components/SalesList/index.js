import React, { useState, useEffect } from 'react';
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
  AutocompleteInput,
  Filter,
  usePermissions,
  DateField,
  ReferenceField,
  ReferenceInput,
  useDataProvider,
  Loading,
} from 'react-admin';
import { getCookie } from '../../api/utils';
import DateMonthInput from '../DateMonthInput';

const SalesListActions = () => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/sales');

  return loaded ? (
    <TopToolbar>
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const SalesFilter = (props) => {
  const { hasBranches } = props;
  return (
    <Filter {...props}>
      {hasBranches ? (
        <ReferenceInput source="branch_id" reference="branches" alwaysOn>
          <AutocompleteInput optionText="address" />
        </ReferenceInput>
      ) : null}
      <ReferenceInput source="product_id" reference="products" alwaysOn>
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
      <DateMonthInput label="From" source="startDate" alwaysOn />
      <DateMonthInput label="To" source="endDate" alwaysOn />
    </Filter>
  );
};

export const SalesCreate = (props) => {
  const dataProvider = useDataProvider();
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dataProvider.getOne('users', { id: parseInt(getCookie('userId'), 10) })
      .then(({ data }) => { setUser(data); setLoading(false); });
  }, []);

  return !loading ? (
    <Create {...props}>
      <SimpleForm>
        <TextInput source="value" label="Amount" />
        {user.role && user.role === 'Администрация' ? (
          <ReferenceInput source="branch_id" reference="branches" alwaysOn>
            <AutocompleteInput optionText="address" />
          </ReferenceInput>
        ) : <TextInput source="branch_id" defaultValue={user.branches[0]} disabled />}
        <ReferenceInput source="product_id" reference="products" alwaysOn>
          <AutocompleteInput optionText="name" />
        </ReferenceInput>
      </SimpleForm>
    </Create>
  ) : <Loading />;
};

export const SalesList = (props) => {
  const dataProvider = useDataProvider();
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    dataProvider.getOne('users', { id: parseInt(getCookie('userId'), 10) })
      .then(({ data }) => { const v = data; setUser(() => v); });
    setLoading(() => false);
  }, []);
  return !loading ? (
    <List {...props} actions={<SalesListActions />} filters={<SalesFilter hasBranches={user.role && user.role !== 'Филиал'} />}>
      <Datagrid>
        <TextField source="id" />
        <DateField source="date" />
        <TextField source="value" label="Amount" />
        <ReferenceField label="Product" source="product_id" reference="products">
          <TextField source="name" />
        </ReferenceField>
        {user.role && user.role !== 'Филиал' ? (
          <ReferenceField label="Branch" source="branch_id" reference="branches">
            <TextField source="address" />
          </ReferenceField>
        ) : null }
      </Datagrid>
    </List>
  ) : null;
};

export default SalesList;
