import React, {Component} from 'react';
import { PropTypes } from 'prop-types';

import './index.css';

class TemperatureMonitor extends Component {
    render() {
        if (this.props.monitor.isLoading)
            return (
                <div>
                    Loading...
                </div>
            );

        if (this.props.monitor.display === "OFF")
            return (
                <div>
                    Display is off
                </div>
            );

        return (
            <div>
                {this.props.monitor.temperature}
            </div>
        )
    }
}

TemperatureMonitor.propTypes = {
    monitor: PropTypes.object.isRequired,
};

export default TemperatureMonitor;
