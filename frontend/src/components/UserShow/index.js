/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
} from 'react-admin';

const UserShow = (props) => (
  <Show title="Showing User" {...props}>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="username" />
    </SimpleShowLayout>
  </Show>
);

export default UserShow;
