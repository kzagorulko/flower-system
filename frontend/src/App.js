import React from 'react';
import {
  Admin, Resource, ShowGuesser,
} from 'react-admin';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import { UserList, UserCreate, UserEdit } from './components/UserList';
import { ProviderList, ProviderCreate, ProviderEdit } from './components/ProviderList';
import UserShow from './components/UserShow';

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
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
