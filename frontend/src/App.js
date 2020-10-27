import React from 'react';
import { Admin, Resource } from 'react-admin';
import dataProvider from './api/dataProvider';
import { UserList, UserCreate, UserEdit } from './components/UserList';
import UserShow from './components/UserShow';

import './App.less';

const App = () => (
  <Admin title="Example" dataProvider={dataProvider('http://127.0.0.1:8000')}>
    <Resource name="users" list={UserList} show={UserShow} create={UserCreate} edit={UserEdit} />
  </Admin>
);

export default App;
