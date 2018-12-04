import {List} from 'immutable';

import ActionTypes from '../constants/actionTypes';

// will be const initialState = fetchDataFromDatabase
const initialState = List();

export const chartData = (state = initialState, action) => {
    switch (action.type) {
        case ActionTypes.CHART_UPDATE:
            return state.push(action.point);
        default:
            return state;
    }
};
