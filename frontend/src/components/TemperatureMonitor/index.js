import React, {Component} from 'react';
import {PropTypes} from 'prop-types';
import Typography from '@material-ui/core/Typography';

import './index.css';

class TemperatureMonitor extends Component {
    render() {
        if (this.props.monitor.display === "OFF")
            return (
                <Typography variant="h3" gutterBottom>
                    Display is off
                </Typography>
            );

        return (
            <div>
                <Typography variant="body1" gutterBottom>
                    Temperature:
                </Typography>
                <Typography variant="h3" gutterBottom>
                    {this.props.monitor.temperature}
                </Typography>
            </div>
        )
    }
}

TemperatureMonitor.propTypes = {
    monitor: PropTypes.object.isRequired,
};

export default TemperatureMonitor;
