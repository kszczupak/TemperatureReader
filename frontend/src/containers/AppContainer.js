import { connect } from 'react-redux';

import { connectToWAMP, subscribeToTemperatureUpdate } from '../actions';
import App from '../components/App';

const mapStateToProps = state => ({});

const mapDispatchToProps = {
    initiateBackend: connectToWAMP,
    subscribeToTemperatureUpdate
};

export const AppContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(App);
