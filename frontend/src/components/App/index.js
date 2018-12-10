import React, { Component } from 'react';

import {TemperatureMonitorContainer} from '../../containers/TemperatureMonitorContainer';
import {TemperatureChartContainer} from "../../containers/TemperatureChartContainer";
import CircularProgress from "@material-ui/core/CircularProgress/CircularProgress";
import Typography from "@material-ui/core/es/Typography/Typography";

import './index.css';


class App extends Component {
    componentDidMount() {
        this.props.initiateBackend();
        this.props.fetchInitialState();
        this.props.fetchInitialChartData();
        this.props.subscribeToStateUpdates();
    }

    loadAndRender = () => {
        if (this.props.isLoading)
            return (
                <div>
                    <CircularProgress />
                    <Typography>
                        Loading Temperature...
                    </Typography>
                </div>
            );

        return (
            <div>
                <TemperatureMonitorContainer/>
                <TemperatureChartContainer/>
            </div>
        );
    };

    render() {
    return (
      <div className="App">
        <header className="App-header">
            {this.loadAndRender()}
        </header>
      </div>
    );
  }
}

export default App;
