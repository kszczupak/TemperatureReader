import React, { Component } from 'react';
import './index.css';

import {TemperatureMonitorContainer} from '../../containers/TemperatureMonitorContainer';


class App extends Component {
    componentDidMount() {
        this.props.initiateBackend();
        // setTimeout(() => this.props.fetchInitialState(), 2000);
        this.props.fetchInitialState();
        this.props.subscribeToStateUpdates();
    }

    render() {
    return (
      <div className="App">
        <header className="App-header">
          <TemperatureMonitorContainer/>
        </header>
      </div>
    );
  }
}

export default App;
