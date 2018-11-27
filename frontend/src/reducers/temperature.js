import ActionTypes from '../constants/actionTypes';

const initialState = {
  isLoading: true,
  value: null
};

export const temperature = (state = initialState, action) => {
  switch (action.type) {
    case ActionTypes.TEMPERATURE_CHANGE:
      return {
        isLoading: false,
        value: action.newTemperatureValue
      };
    default:
      return state;
  }
};
