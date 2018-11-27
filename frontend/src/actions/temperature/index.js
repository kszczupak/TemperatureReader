import ActionTypes from '../../constants/actionTypes';
import config from '../../config.json';
import {subscribe} from '../index';


const temperatureUpdate = newTemperatureValue => ({
        type: ActionTypes.TEMPERATURE_CHANGE,
        newTemperatureValue
    });

export const subscribeToTemperatureUpdate = () => (dispatch, getState) => {
    const topic = config.crossbar.topic;

    const handleTemperatureUpdate = newTemperatureValue => {
        dispatch(temperatureUpdate(newTemperatureValue))
    };

    return subscribe(
        topic,
        handleTemperatureUpdate
    );
};
