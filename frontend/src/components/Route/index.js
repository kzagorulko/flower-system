import React from 'react';
import { Route as ReactRoute } from 'react-router-dom';

const Route = ({
  path,
  exact,
  component: Component,
}) => (
  <ReactRoute exact={exact} path={path}>
    <Component />
  </ReactRoute>
);

export default Route;
