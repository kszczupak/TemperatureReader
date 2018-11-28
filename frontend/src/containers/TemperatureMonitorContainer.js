import { connect } from 'react-redux';

import TemperatureMonitor from '../components/TemperatureMonitor';

const mapStateToProps = state => ({
    monitor: state.monitor,
});

export const TemperatureMonitorContainer = connect(
    mapStateToProps
)(TemperatureMonitor);
