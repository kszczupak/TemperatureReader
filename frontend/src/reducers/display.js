import ActionTypes from '../constants/actionTypes';

const initialState = null;

export const display = (state = initialState, action) => {
  switch (action.type) {
    case ActionTypes.DISPLAY_CHANGE:
      return action.newDisplayState;
    default:
      return state;
  }
};
