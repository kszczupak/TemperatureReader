import { combineReducers } from 'redux';

import { temperature } from './temperature';
import {display} from './display';
import { wampConnection } from './wampConnection';

export default combineReducers({
  temperature,
  display,
  wampConnection
});
