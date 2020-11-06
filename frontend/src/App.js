import React from 'react';
import { Admin, Resource } from 'react-admin';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import { UserList, UserCreate, UserEdit } from './components/UserList';
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
    ]}
  </Admin>
);

export default App;
