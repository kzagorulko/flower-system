import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.less';

const App = () => (
  <div>
    <Router>
      <Switch>
        <Route path="/flower">
          <h1>Flower</h1>
        </Route>
        <Route path="/system">
          <h1>System</h1>
        </Route>
        <Route exact path="/">
          <h1>Flower System</h1>
        </Route>
        <Route path="*">
          <h1> No such page </h1>
        </Route>
      </Switch>
    </Router>
  </div>
);

export default App;
