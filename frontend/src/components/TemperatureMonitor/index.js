import React, {Component} from 'react';
import { PropTypes } from 'prop-types';
import Typography from '@material-ui/core/Typography';

import './index.css';

class TemperatureMonitor extends Component {
    render() {
        if (this.props.monitor.display === "OFF")
            return (
                <div>
                    Display is off
                </div>
            );

        return (
            <Typography variant="headline" align="center">
                {this.props.monitor.temperature}
            </Typography>
        )
    }
}

TemperatureMonitor.propTypes = {
    monitor: PropTypes.object.isRequired,
};

export default TemperatureMonitor;
