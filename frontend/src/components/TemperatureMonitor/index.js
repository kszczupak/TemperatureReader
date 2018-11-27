import React, {Component} from 'react';
import { PropTypes } from 'prop-types';

import './index.css';

class TemperatureMonitor extends Component {
    render() {
        if (this.props.temperature.isLoading)
            return (
                <div>
                    Loading...
                </div>
            );

        return (
            <div>
                {this.props.temperature.value}
            </div>
        )
    }
}

TemperatureMonitor.propTypes = {
  temperature: PropTypes.object.isRequired
};

export default TemperatureMonitor;
