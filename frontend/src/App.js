import React from 'react';
import { Admin, Resource } from 'react-admin';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';
import { UserList, UserCreate, UserEdit } from './components/UserList';
import UserShow from './components/UserShow';

import './App.less';

const App = () => (
  <Admin title="Example" dataProvider={dataProvider} authProvider={authProvider}>
    <Resource name="users" list={UserList} show={UserShow} create={UserCreate} edit={UserEdit} />
  </Admin>
);

export default App;
