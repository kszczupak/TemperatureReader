import { connect } from 'react-redux';

import { startPeriodicChartUpdates, stopPeriodicChartUpdates, fetchInitialChartData } from '../actions';
import TemperatureChart from '../components/TemperatureChart';

const mapStateToProps = state => ({
    isLoading: state.chartData.isLoading,
    data: state.chartData.data.toJS()
});

const mapDispatchToProps = {
    startPeriodicChartUpdates,
    stopPeriodicChartUpdates,
    fetchInitialChartData
};

export const TemperatureChartContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(TemperatureChart);
