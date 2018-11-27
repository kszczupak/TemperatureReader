import ActionTypes from '../constants/actionTypes';
import { stage } from '../constants/connection';

const initialState = {
  stage: stage.NOT_CONNECTED,
  connected: false,
  session: null
};

export const wampConnection = (state = initialState, action) => {
  switch (action.type) {
    case ActionTypes.WAMP_CONNECTION_INITIATED:
      return {
        ...state,
        stage: stage.CONNECTING
      };
    case ActionTypes.WAMP_CONNECTION_SUCCESS:
      return {
        ...state,
        stage: stage.CONNECTED,
        connected: true,
        session: action.session
      };
    case ActionTypes.WAMP_ERROR:
      return {
        ...state,
        stage: stage.ERROR,
        connected: false
      };
    default:
      return state;
  }
};
