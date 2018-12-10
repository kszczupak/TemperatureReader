import { connect } from 'react-redux';

import {connectToWAMP, subscribeToMonitorUpdates, getCurrentMonitorState, fetchInitialChartData} from '../actions';
import App from '../components/App';

const mapStateToProps = state => ({
    isLoading: state.monitor.isLoading
});

const mapDispatchToProps = {
    initiateBackend: connectToWAMP,
    fetchInitialState: getCurrentMonitorState,
    subscribeToStateUpdates: subscribeToMonitorUpdates,
    fetchInitialChartData
};

export const AppContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(App);
