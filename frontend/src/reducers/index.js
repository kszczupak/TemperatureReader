import { combineReducers } from 'redux';

import { temperature } from './temperature';
import { wampConnection } from './wampConnection';

export default combineReducers({
  temperature,
  wampConnection
});
