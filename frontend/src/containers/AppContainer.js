import { connect } from 'react-redux';

import { connectToWAMP, subscribeToMonitorUpdates, getCurrentMonitorState } from '../actions';
import App from '../components/App';

const mapStateToProps = state => ({});

const mapDispatchToProps = {
    initiateBackend: connectToWAMP,
    fetchInitialState: getCurrentMonitorState,
    subscribeToStateUpdates: subscribeToMonitorUpdates
};

export const AppContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(App);
