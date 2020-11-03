/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
  useNotify,
  BooleanField,
} from 'react-admin';

const UserShow = (props) => {
  const notify = useNotify();
  const clickie = () => notify('Clicked', 'info');
  return (
    <Show title="Showing User" {...props}>
      <SimpleShowLayout>
        <TextField source="id" onClick={clickie} />
        <TextField source="username" />
        <TextField source="displayName" />
        <BooleanField source="deactivated" />
        <TextField source="email" />
      </SimpleShowLayout>
    </Show>
  );
};

export default UserShow;
