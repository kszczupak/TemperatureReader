import { combineReducers } from 'redux';

import { monitor } from './monitor';
import { wampConnection } from './wampConnection';

export default combineReducers({
  monitor,
  wampConnection
});
