import {callRPC, waitForWampReady} from '../index';
import ActionTypes from '../../constants/actionTypes';
import config from '../../config';
import {store} from '../../store';

export const updateChartData = newValue => ({
    type: ActionTypes.CHART_UPDATE,
    point: {
        x: new Date(),
        y: newValue
    }
});

const initializeChartData = rawData => ({
    type: ActionTypes.CHART_INIT,
    rawData
});

let chartUpdatesInterval = null;

export const startPeriodicChartUpdates = () => (dispatch, getState) => {
    chartUpdatesInterval = setInterval(
        () => dispatch(updateChartData(getState().monitor.temperature)),
        config.chart.updateIntervalInSec * 1000
    );
};

export const stopPeriodicChartUpdates = () => () => {
    clearInterval(chartUpdatesInterval);
};

export const resetCurrentChartUpdate = () => {
    clearInterval(chartUpdatesInterval);
    chartUpdatesInterval = setInterval(
        () => store.dispatch(updateChartData(store.getState().monitor.temperature)),
        config.chart.updateIntervalInSec * 1000
    );
};

export const fetchInitialChartData = () => (dispatch) => {
    return waitForWampReady(() => {
        return callRPC(
            config.crossbar.endpoints.lastReadings
        ).then(
            response => JSON.parse(response)
        ).then(
            response => {
                dispatch(initializeChartData(response));
            }
        )
    })
};
