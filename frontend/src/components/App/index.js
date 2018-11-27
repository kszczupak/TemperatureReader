import React, { Component } from 'react';
import './index.css';

import {TemperatureMonitorContainer} from '../../containers/TemperatureMonitorContainer';


class App extends Component {
    componentDidMount() {
        this.props.initiateBackend();
        // setTimeout(() => {
        //     this.props.subscribeToTemperatureUpdate()
        // },
        //     3000
        // );
        this.props.subscribeToTemperatureUpdate();

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
