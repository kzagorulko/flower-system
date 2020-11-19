import React, { useEffect, useState } from 'react';

import classNames from 'classnames/bind';
import {
  List,
  useListContext,
  usePermissions,
  TopToolbar,
  CreateButton,
  Filter,
  TextInput,
  Datagrid,
  TextField,
  Show,
  Create,
  SimpleForm,
  SelectInput,
  useNotify,
  BooleanField,
} from 'react-admin';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import { getCookie } from '../../api/utils';
import dataProvider from '../../api/dataProvider';
import UserCard from '../UserCard';
import style from './style.less';
import QuickFilter from '../QuickFilter';

const cx = classNames.bind(style);

const departmentChoices = [
  { id: 1, name: 'Администрация' },
  { id: 2, name: 'Отдел продаж' },
  { id: 3, name: 'Юридический отдел' },
  { id: 4, name: 'Отдел логистики' },
];

const finalStatusChoices = ['CANCELLED', 'DONE'];

const statusChoices = [
  { id: 'IN_PROGRESS', name: 'В работе' },
  { id: 'CANCELLED', name: 'Отменена' },
  { id: 'DONE', name: 'Завершена' },
];

const viewTypeChoices = [
  { id: 'INBOX', name: 'Входящие' },
  { id: 'OUTBOX', name: 'Исходящие' },
  { id: 'EXECUTOR', name: 'Я исполнитель' },
];

const RequestListActions = ({
  filters, resource, showFilter, displayedFilters, filterValues,
}) => {
  const {
    basePath,
  } = useListContext();
  const { loaded, permissions } = usePermissions('/requests');

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

const RequestFilters = (props) => (
  <Filter {...props}>
    <TextInput label="Поиск" source="name" alwaysOn />
    <SelectInput label="Вид отображения" source="view" choices={viewTypeChoices} />
    <QuickFilter label="Без исполнителя" source="noExecutor" defaultValue />
  </Filter>
);

export const RequestList = (props) => (
  <List
    {...props}
    actions={<RequestListActions />}
    filters={<RequestFilters />}
    sort={{ field: 'created', order: 'DESC' }}
  >
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="department" />
      <TextField source="status" />
      <TextField source="created" />
      <BooleanField source="hasExecutor" />
    </Datagrid>
  </List>
);

export const RequestShow = (props) => {
  const { id } = props;

  const notify = useNotify();

  const [record, setRecord] = useState({});
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState({});

  useEffect(() => {
    dataProvider.getOne('requests', { id })
      .then(({ data }) => { const v = data; setRecord(() => v); });
    dataProvider.getOne('users', { id: parseInt(getCookie('userId'), 10) })
      .then(({ data }) => { const v = data; setUser(() => v); });
    setLoading(() => false);
  }, [id, loading]);

  return (record && record.creator && !loading) ? (
    <Show title={`Заявка №${id}`} {...props}>
      <SimpleForm toolbar={<div />}>
        <TextField record={record} source="id" />
        <TextField record={record} source="name" />
        <TextField record={record} source="department" />
        { (record.executor && record.executor.id === parseInt(getCookie('userId'), 10)
          && !finalStatusChoices.includes(record.statusCode)) ? (
            <SelectInput
              record={record}
              source="statusCode"
              choices={statusChoices}
              onChange={(e) => dataProvider.updateStatus('requests', { id, status: e.target.value })
                .then(() => setLoading(() => true))}
              label="Статус"
            />
          ) : <TextField record={record} source="status" /> }
        <TextField record={record} source="created" />
        <TextField record={record} source="description" />
        <TextField record={record} source="category" />
        <div>
          <Typography variant="caption" component="div" color="textSecondary">Создатель заявка</Typography>
          <UserCard user={record.creator} />
        </div>
        <div>
          <Typography variant="caption" component="div" color="textSecondary">Исполнитель</Typography>
          { record.executor ? <UserCard user={record.executor} />
            : (user.role === record.department && (
              <Button
                href=""
                className={cx('Button')}
                variant="contained"
                color="secondary"
                onClick={() => dataProvider.update('requests', { id })
                  .then(() => setRecord(() => {
                    setLoading(() => true);
                    return { executor_id: parseInt(getCookie('userId'), 10), ...record };
                  }))
                  .catch((err) => notify(err.message, 'error'))}
              >
                Стать исполнителем
              </Button>
            )) || <Typography component="div">Исполнитель на заявку пока не найден</Typography>}
        </div>
      </SimpleForm>
    </Show>
  ) : null;
};

export const RequestCreate = (props) => {
  const [requestCategories, setCategories] = useState([]);
  useEffect(() => {
    dataProvider.getList('requests/categories')
      .then(({ data }) => { const v = data; setCategories(() => v); });
  }, []);
  return (
    <Create {...props}>
      <SimpleForm>
        <TextInput source="name" />
        <TextInput multiline source="description" />
        <SelectInput source="department_id" choices={departmentChoices} />
        <SelectInput source="category_id" choices={requestCategories} />
      </SimpleForm>
    </Create>
  );
};
