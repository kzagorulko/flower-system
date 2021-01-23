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
  Filter,
  usePermissions,
  Show,
  ReferenceField,
  DateField,
  SelectInput,
  ReferenceInput,
  AutocompleteInput,
  NumberInput,
  useDataProvider,
  DateInput,
  useNotify,
} from 'react-admin';
import { getCookie } from '../../api/utils';
import DateMonthInput from '../DateMonthInput';

const statusChoices = [
  { id: 'IN_PROGRESS', name: 'В работе' },
  { id: 'CANCELLED', name: 'Отменена' },
  { id: 'DONE', name: 'Завершена' },
];

const finalStatusChoices = ['CANCELLED', 'DONE'];

const SuppliesListActions = ({
  filters,
  resource,
  showFilter,
  displayedFilters,
  filterValues,
}) => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/supplies');

  return loaded ? (
    <TopToolbar>
      {(filters) && React.cloneElement(filters, {
        resource,
        showFilter,
        displayedFilters,
        filterValues,
        context: 'button',
        label: 'label',
      })}
      {permissions.actions.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

const SuppliesFilter = (props) => {
  const { hasBranches } = props;
  return (
    <Filter {...props}>
      <ReferenceInput source="branch_id" reference="branches" alwaysOn>
        <AutocompleteInput optionText="address" />
      </ReferenceInput>
      {hasBranches ? (
        <ReferenceInput source="warehouse_id" reference="warehouses">
          <AutocompleteInput optionText="address" />
        </ReferenceInput>
      ) : null}
      <ReferenceInput source="product_id" reference="products" alwaysOn>
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
      <DateMonthInput label="From" source="startDate" />
      <DateMonthInput label="To" source="endDate" />
    </Filter>
  );
};

export const SupplyCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <ReferenceInput source="branch_id" reference="branches">
        <AutocompleteInput optionText="address" />
      </ReferenceInput>
      <ReferenceInput source="warehouse_id" reference="warehouses">
        <AutocompleteInput optionText="address" />
      </ReferenceInput>
      <ReferenceInput source="product_id" reference="products">
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
      <NumberInput source="value" min="0" />
      <DateInput source="date" />
    </SimpleForm>
  </Create>
);

export const SupplyShow = (props) => {
  const { id } = props;
  const dataProvider = useDataProvider();
  const { loaded, permissions } = usePermissions('/supplies');
  const [record, setRecord] = useState({});
  const [loading, setLoading] = useState(true);
  const notify = useNotify();

  useEffect(() => {
    dataProvider.getOne('supplies', { id })
      .then(({ data }) => setRecord(data));
    setLoading(false);
  }, [id, loading]);

  return (!loading && loaded) ? (
    <Show {...props}>
      <SimpleForm toolbar={<div />}>
        <ReferenceField link="show" label="Product" source="product_id" reference="products">
          <TextField source="name" />
        </ReferenceField>
        <ReferenceField link="show" label="Warehouse" source="warehouse_id" reference="warehouses">
          <TextField source="address" />
        </ReferenceField>
        {/* to omit for branch users when backend branch filtering added */}
        <ReferenceField link="show" label="Branch" source="branch_id" reference="branches">
          <TextField source="address" />
        </ReferenceField>
        <TextField source="value" />
        { (permissions.actions.includes('update') && !finalStatusChoices.includes(record.status)) ? (
          <SelectInput
            source="status"
            choices={statusChoices}
            onChange={(e) => dataProvider.update('supplies', { id, data: { status: e.target.value }, updateStatus: true })
              .then(() => setLoading(() => true))
              .catch((err) => notify(err.message, 'error'))}
          />
        ) : <TextField source="status" /> }
      </SimpleForm>
    </Show>
  ) : null;
};

export const SuppliesList = (props) => {
  const dataProvider = useDataProvider();
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    dataProvider.getOne('users', { id: parseInt(getCookie('userId'), 10) })
      .then(({ data }) => { setUser(data); setLoading(false); });
  }, []);
  return (!loading) ? (
    <List
      {...props}
      actions={<SuppliesListActions />}
      bulkActionButtons={false}
      filters={<SuppliesFilter hasBranches={user.role && user.role !== 'Филиал'} />}
    >
      {/* search by product_id, warehouse_id, branch_id, startendDate */}
      <Datagrid rowClick="show">
        <TextField source="id" />
        <DateField source="date" showTime />
        <ReferenceField link="show" label="Product" source="product_id" reference="products">
          <TextField source="name" />
        </ReferenceField>
        <ReferenceField link="show" label="Branch" source="branch_id" reference="branches">
          <TextField source="address" />
        </ReferenceField>
        {user.role && user.role !== 'Филиал' ? (
          <ReferenceField link="show" label="Warehouse" source="warehouse_id" reference="warehouses">
            <TextField source="address" />
          </ReferenceField>
        ) : null }
        <TextField source="value" />
        <TextField source="status" />
      </Datagrid>
    </List>
  ) : null;
};

export default SuppliesList;
