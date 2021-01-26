import React, { useEffect, useState } from 'react';
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
  ReferenceField,
  ReferenceInput,
  AutocompleteInput,
  DateField,
  NumberInput,
  DateInput,
  SelectInput,
  useDataProvider,
  useNotify,
} from 'react-admin';
import DateMonthInput from '../DateMonthInput';

const statusChoices = [
  { id: 'IN_PROGRESS', name: 'В работе' },
  { id: 'CANCELLED', name: 'Отменена' },
  { id: 'DONE', name: 'Завершена' },
];

const finalStatusChoices = ['CANCELLED', 'DONE'];

const PurchasesListActions = ({
  filters,
  resource,
  showFilter,
  displayedFilters,
  filterValues,
  permissions,
}) => {
  const {
    basePath,
  } = useListContext();
  return (
    <TopToolbar>
      {(filters) && React.cloneElement(filters, {
        resource,
        showFilter,
        displayedFilters,
        filterValues,
        context: 'button',
        label: 'label',
      })}
      {permissions.purchases.includes('create') ? <CreateButton basePath={basePath} /> : null}
    </TopToolbar>
  );
};

const PurchasesFilter = (props) => {
  const { permissions } = props;
  return (
    <Filter {...props}>
      { permissions.contracts ? (
        <ReferenceInput source="contract_id" reference="contracts" alwaysOn>
          <AutocompleteInput optionText="number" />
        </ReferenceInput>
      ) : null }
      { permissions.warehouses ? (
        <ReferenceInput source="warehouse_id" reference="warehouses">
          <AutocompleteInput optionText="address" />
        </ReferenceInput>
      ) : null }
      { permissions.products ? (
        <ReferenceInput source="product_id" reference="products" alwaysOn>
          <AutocompleteInput optionText="name" />
        </ReferenceInput>
      ) : null }
      <DateMonthInput label="From" source="startDate" />
      <DateMonthInput label="To" source="endDate" />
    </Filter>
  );
};

export const PurchaseCreate = (props) => (
  <Create {...props}>
    <SimpleForm>
      <ReferenceInput source="warehouse_id" reference="warehouses">
        <AutocompleteInput optionText="address" />
      </ReferenceInput>
      <TextInput source="address" />
      <ReferenceInput source="product_id" reference="products">
        <AutocompleteInput optionText="name" />
      </ReferenceInput>
      <ReferenceInput source="contract_id" reference="contracts">
        <AutocompleteInput optionText="number" />
      </ReferenceInput>
      <NumberInput source="value" min="0" />
      <DateInput source="date" />
    </SimpleForm>
  </Create>
);

export const PurchaseShow = (props) => {
  const { id } = props;
  const dataProvider = useDataProvider();
  const { loaded, permissions } = usePermissions();
  const [record, setRecord] = useState({});
  const [loading, setLoading] = useState(true);
  const notify = useNotify();

  useEffect(() => {
    dataProvider.getOne('purchases', { id })
      .then(({ data }) => setRecord(data));
    setLoading(false);
  }, [id, loading]);

  return (!loading && loaded) ? (
    <Show {...props}>
      <SimpleForm toolbar={<div />}>
        { permissions.contracts ? (
          <ReferenceField link="show" label="Contract" source="contract_id" reference="contracts">
            <TextField source="number" />
          </ReferenceField>
        ) : null}
        { permissions.products ? (
          <ReferenceField link="show" label="Product" source="product_id" reference="products">
            <TextField source="name" />
          </ReferenceField>
        ) : null }
        { permissions.purchases.includes('update_warehouse') ? (
          <ReferenceInput source="warehouse_id" reference="warehouses">
            <AutocompleteInput
              optionText="address"
              onSelect={(e) => dataProvider.update('purchases', { id, data: { warehouse_id: e.id }, subresource: 'warehouse' })
                .then(() => setLoading(() => true))
                .catch((err) => notify(err.message, 'error'))}
            />
          </ReferenceInput>
        ) : null}
        <TextField source="value" />
        <TextField source="value" />
        { (permissions.purchases.includes('update_status') && !finalStatusChoices.includes(record.status)) ? (
          <SelectInput
            source="status"
            choices={statusChoices}
            onChange={(e) => dataProvider.update('purchases', { id, data: { status: e.target.value }, subresource: 'status' })
              .then(() => setLoading(() => true))
              .catch((err) => notify(err.message, 'error'))}
          />
        ) : <TextField source="status" /> }
      </SimpleForm>
    </Show>
  ) : null;
};

export const PurchasesList = (props) => {
  const { loaded, permissions } = usePermissions();
  return loaded ? (
    <List
      {...props}
      actions={<PurchasesListActions permissions={permissions} />}
      bulkActionButtons={false}
      filters={<PurchasesFilter permissions={permissions} />}
    >
      <Datagrid rowClick="show">
        <TextField source="id" />
        <DateField source="date" showTime />
        { permissions.warehouses ? (
          <ReferenceField link="show" label="Warehouse" source="warehouse_id" reference="warehouses">
            <TextField source="address" />
          </ReferenceField>
        ) : null }
        { permissions.contracts ? (
          <ReferenceField link="show" label="Contract" source="contract_id" reference="contracts">
            <TextField source="number" />
          </ReferenceField>
        ) : null }
        { permissions.products ? (
          <ReferenceField link="show" label="Product" source="product_id" reference="products">
            <TextField source="name" />
          </ReferenceField>
        ) : null }
        <TextField source="value" />
        <TextField source="status" />
      </Datagrid>
    </List>
  ) : null;
};

export default PurchasesList;
