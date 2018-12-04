import {callRPC, waitForWampReady} from '../index';
import ActionTypes from '../../constants/actionTypes';
import config from '../../config';

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
        config.chart.updateIntervalInSec * 1000   // 30s
    );
};

export const stopPeriodicChartUpdates = () => () => {
    clearInterval(chartUpdatesInterval);
};

export const fetchInitialChartData = () => (dispatch, getState) => {
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
