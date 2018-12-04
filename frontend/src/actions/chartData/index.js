import ActionTypes from '../../constants/actionTypes';

export const updateChartData = newValue => ({
    type: ActionTypes.CHART_UPDATE,
    point: {
        x: new Date(),
        y: newValue
    }
});

let chartUpdatesInterval = null;

export const startPeriodicChartUpdates = () => (dispatch, getState) => {
    chartUpdatesInterval = setInterval(
        () => dispatch(updateChartData(getState().monitor.temperature)),
        30000   // 30s
    );
};

export const stopPeriodicChartUpdates = () => () => {
    clearInterval(chartUpdatesInterval);
};
