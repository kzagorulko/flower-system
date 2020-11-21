import React from 'react';
import {
  Admin, Resource, ShowGuesser,
} from 'react-admin';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import {
  UserList,
  UserCreate,
  UserEdit,
  UserShow,
} from './components/UserList';
import { ProviderList, ProviderCreate, ProviderEdit } from './components/ProviderList';
import { ProductList, ProductCreate, ProductEdit } from './components/ProductsList';
import { RequestList, RequestShow, RequestCreate } from './components/Requests';
import {
  RequestCategoryList,
  RequestCategoryCreate,
  RequestCategoryShow,
  RequestCategoryEdit,
} from './components/RequestCategories';

import './App.less';

const App = () => (
  <Admin title="Flower System" dataProvider={dataProvider} authProvider={authProvider}>
    {(permissions) => [
      permissions.users
        ? (
          <Resource
            name="users"
            list={UserList}
            show={UserShow}
            create={permissions.users.includes('create') ? UserCreate : null}
            edit={permissions.users.includes('update') ? UserEdit : null}
            options={{ label: 'Пользователи' }}
          />
        ) : null,
      permissions.providers
        ? (
          <Resource
            name="providers"
            list={ProviderList}
            show={ShowGuesser}
            create={permissions.providers.includes('create') ? ProviderCreate : null}
            edit={permissions.providers.includes('update')
              || permissions.providers.includes('update_status') ? ProviderEdit : null}
            options={{ label: 'Поставщики' }}
          />
        ) : null,
      permissions.products
        ? (
          <Resource
            name="products"
            list={ProductList}
            show={ShowGuesser}
            create={permissions.products.includes('create') ? ProductCreate : null}
            edit={permissions.products.includes('update') ? ProductEdit : null}
            options={{ label: 'Продукты' }}
          />
        ) : null,
      permissions.requests
        ? (
          <Resource
            name="requests"
            list={RequestList}
            show={RequestShow}
            create={permissions.requests.includes('create') ? RequestCreate : null}
            options={{ label: 'Заявки' }}
          />
        ) : null,
      permissions.requests.includes('create_category')
        ? (
          <Resource
            name="requestCategories"
            list={RequestCategoryList}
            create={RequestCategoryCreate}
            show={RequestCategoryShow}
            edit={RequestCategoryEdit}
            options={{ label: 'Категории заявок' }}
          />
        ) : null,
      permissions.branches
        ? (
          <Resource
            name="branches"
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
