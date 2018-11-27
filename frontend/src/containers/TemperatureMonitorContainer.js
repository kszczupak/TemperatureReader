import { connect } from 'react-redux';

import TemperatureMonitor from '../components/TemperatureMonitor';

const mapStateToProps = state => ({
    temperature: state.temperature
});

export const TemperatureMonitorContainer = connect(
    mapStateToProps
)(TemperatureMonitor);
