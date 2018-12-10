import { connect } from 'react-redux';

import { startPeriodicChartUpdates, stopPeriodicChartUpdates } from '../actions';
import TemperatureChart from '../components/TemperatureChart';

const mapStateToProps = state => ({
    isLoading: state.chartData.isLoading,
    data: state.chartData.data.toJS()
});

const mapDispatchToProps = {
    startPeriodicChartUpdates,
    stopPeriodicChartUpdates,
};

export const TemperatureChartContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(TemperatureChart);
