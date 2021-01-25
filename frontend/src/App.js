import React from 'react';
import {
  Admin, Resource,
} from 'react-admin';
import UserIcon from '@material-ui/icons/Group';
import InboxIcon from '@material-ui/icons/Inbox';
import AccountTreeIcon from '@material-ui/icons/AccountTree';
import CategoryIcon from '@material-ui/icons/Category';
import TrendingUpIcon from '@material-ui/icons/TrendingUp';
import AddShoppingCartIcon from '@material-ui/icons/AddShoppingCart';
import DepartureBoardIcon from '@material-ui/icons/DepartureBoard';
import LocalShippingIcon from '@material-ui/icons/LocalShipping';
import HomeWorkIcon from '@material-ui/icons/HomeWork';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import {
  UserList,
  UserCreate,
  UserEdit,
  UserShow,
} from './components/UserList';
import {
  ProviderList,
  ProviderCreate,
  ProviderEdit,
  ProviderShow,
} from './components/ProviderList';
import {
  ProductList,
  ProductCreate,
  ProductEdit,
  ProductShow,
} from './components/ProductsList';
import {
  WarehouseList,
  WarehouseCreate,
  WarehouseEdit,
  WarehouseShow,
} from './components/WarehouseList';
import {
  BranchesList,
  BranchCreate,
  BranchShow,
  BranchEdit,
} from './components/BranchesList';
import {
  SuppliesList,
  SupplyCreate,
  SupplyShow,
} from './components/SuppliesList';
import {
  PurchasesList,
  PurchaseCreate,
  PurchaseShow,
} from './components/PurchasesList';
import { RequestList, RequestShow, RequestCreate } from './components/Requests';
import {
  RequestCategoryList,
  RequestCategoryCreate,
  RequestCategoryShow,
  RequestCategoryEdit,
} from './components/RequestCategories';
import { SalesList, SalesCreate, SalesShow } from './components/SalesList';
import {
  ContractList,
  ContractShow,
  ContractCreate,
  ContractEdit,
} from './components/Contracts';

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
            icon={UserIcon}
            options={{ label: 'Пользователи' }}
          />
        ) : null,
      permissions.providers
        ? (
          <Resource
            name="providers"
            list={ProviderList}
            show={ProviderShow}
            create={permissions.providers.includes('create') ? ProviderCreate : null}
            edit={permissions.providers.includes('update')
              || permissions.providers.includes('update_status') ? ProviderEdit : null}
            icon={LocalShippingIcon}
            options={{ label: 'Поставщики' }}
          />
        ) : null,
      permissions.products
        ? (
          <Resource
            name="products"
            list={ProductList}
            show={ProductShow}
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
            icon={InboxIcon}
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
            icon={CategoryIcon}
            options={{ label: 'Категории заявок' }}
          />
        ) : null,
      permissions.branches
        ? (
          <Resource
            name="branches"
            list={BranchesList}
            show={BranchShow}
            create={permissions.branches.includes('create') ? BranchCreate : null}
            edit={permissions.branches.includes('update') ? BranchEdit : null}
            icon={AccountTreeIcon}
            options={{ label: 'Филиалы' }}
          />
        ) : null,
      permissions.supplies
        ? (
          <Resource
            name="supplies"
            list={SuppliesList}
            show={SupplyShow}
            create={permissions.supplies.includes('create') ? SupplyCreate : null}
            icon={DepartureBoardIcon}
            options={{ label: 'Поставки' }}
          />
        ) : null,
      permissions.sales
        ? (
          <Resource
            name="sales"
            list={SalesList}
            create={permissions.sales.includes('create') ? SalesCreate : null}
            show={SalesShow}
            icon={TrendingUpIcon}
            options={{ label: 'Продажи' }}
          />
        ) : null,
      permissions.purchases
        ? (
          <Resource
            name="purchases"
            list={PurchasesList}
            create={permissions.purchases.includes('create') ? PurchaseCreate : null}
            show={PurchaseShow}
            icon={AddShoppingCartIcon}
            options={{ label: 'Закупки' }}
          />
        ) : null,
      permissions.warehouses
        ? (
          <Resource
            name="warehouses"
            list={WarehouseList}
            create={permissions.warehouses.includes('create') ? WarehouseCreate : null}
            show={WarehouseShow}
            edit={permissions.warehouses.includes('update') ? WarehouseEdit : null}
            icon={HomeWorkIcon}
            options={{ label: 'Склады' }}
          />) : null,
      permissions.contracts
        ? (
          <Resource
            name="contracts"
            list={ContractList}
            show={ContractShow}
            create={permissions.contracts.includes('create') ? ContractCreate : null}
            edit={permissions.contracts.includes('update') ? ContractEdit : null}
            options={{ label: 'Контракты' }}
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
