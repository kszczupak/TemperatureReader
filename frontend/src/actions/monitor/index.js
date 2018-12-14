import ActionTypes from '../../constants/actionTypes';
import config from '../../config.json';
import {subscribe, callRPC, waitForWampReady} from '../index';
import {updateChartData} from "../index";

const temperatureChange = newTemperatureValue => ({
    type: ActionTypes.TEMPERATURE_CHANGE,
    newTemperatureValue
});

const displayChange = newDisplayState => ({
    type: ActionTypes.DISPLAY_CHANGE,
    newDisplayState
});

export const subscribeToMonitorUpdates = () => (dispatch) => {
    const handleTemperatureUpdate = rawTemperature => {
        const parsedTemperature = JSON.parse(rawTemperature);

        dispatch(temperatureChange(parsedTemperature));
        dispatch(updateChartData(parsedTemperature));
    };

    const handleDisplayChange = newDisplayState => {
        dispatch(displayChange(newDisplayState))
    };

    waitForWampReady( () => subscribe(
        config.crossbar.topics.temperature,
        handleTemperatureUpdate
        )
    );

    waitForWampReady(() => subscribe(
        config.crossbar.topics.display,
        handleDisplayChange
        )
    );
};

export const getCurrentMonitorState = () => (dispatch) => {
    return waitForWampReady(() => {
        return callRPC(
            config.crossbar.endpoints.currentState
        ).then(
            response => JSON.parse(response)
        ).then(
            response => {
                dispatch(temperatureChange(response.temperature));
                dispatch(displayChange(response.display));
            }
        )
    })
};
