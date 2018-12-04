import { combineReducers } from 'redux';

import { monitor } from './monitor';
import { wampConnection } from './wampConnection';
import {chartData} from "./chartData";

export default combineReducers({
  monitor,
  wampConnection,
  chartData
});
