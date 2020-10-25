import React from 'react';
import { BrowserRouter as Router, Switch } from 'react-router-dom';
import Route from './components/Route';
import HomePage from './routes/HomePage';
import './App.less';

const Hello = () => (
  <h1> Hello </h1>
);

const NoPage = () => (
  <h1> No such page </h1>
);

const App = () => (
  <div>
    <Router>
      <Switch>
        <Route path="/flower" component={Hello} />
        <Route path="/system" component={Hello} />
        <Route exact path="/" component={HomePage} />
        <Route path="*" component={NoPage} />
      </Switch>
    </Router>
  </div>
);

export default App;
