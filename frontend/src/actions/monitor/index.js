import ActionTypes from '../../constants/actionTypes';
import config from '../../config.json';
import {subscribe, callRPC, waitForWampReady} from '../index';


const temperatureChange = newTemperatureValue => ({
    type: ActionTypes.TEMPERATURE_CHANGE,
    newTemperatureValue
});

const displayChange = newDisplayState => ({
    type: ActionTypes.DISPLAY_CHANGE,
    newDisplayState
});

export const subscribeToMonitorUpdates = () => (dispatch, getState) => {
    const handleTemperatureUpdate = newTemperatureValue => {
        dispatch(temperatureChange(newTemperatureValue))
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

export const getCurrentMonitorState = () => (dispatch, getState) => {
    return waitForWampReady(() => {
        return callRPC(
            config.crossbar.endpoints.currentState
        ).then(
            response => JSON.parse(response)
        ).then(
            response => {
                dispatch(temperatureChange(response.temperature));
                dispatch(displayChange(response.display))
            }
        )
    })
};
