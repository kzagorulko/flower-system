/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
  useNotify,
} from 'react-admin';

const UserShow = (props) => {
  const notify = useNotify();
  const clickie = () => notify('Clicked', 'info');
  return (
    <Show title="Showing User" {...props}>
      <SimpleShowLayout>
        <TextField source="id" onClick={clickie} />
        <TextField source="username" />
      </SimpleShowLayout>
    </Show>
  );
};

export default UserShow;
