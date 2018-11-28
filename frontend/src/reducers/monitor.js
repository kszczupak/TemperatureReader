import ActionTypes from '../constants/actionTypes';

const initialState = {
  isLoading: true,
  temperature: null,
  display: null
};

export const monitor = (state = initialState, action) => {
  switch (action.type) {
      case ActionTypes.TEMPERATURE_CHANGE:
        return {
          ...state,
          isLoading: false,
          temperature: action.newTemperatureValue
        };
      case ActionTypes.DISPLAY_CHANGE:
          return {
            ...state,
              display: action.newDisplayState
          };
    default:
      return state;
  }
};
