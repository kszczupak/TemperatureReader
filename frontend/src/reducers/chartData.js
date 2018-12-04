import {List} from 'immutable';

import ActionTypes from '../constants/actionTypes';
import config from '../config';

const initialState = {
    isLoading: true,
    data: List()
};

/**
 * Converts raw temperature readings with timestamps to chart data.
 * Conversion is done with respect to set update interval and chart data limit.
 * @param rawData Array of temperature changes with timestamps
 * @returns {Immutable.List<any>} Parsed chart data (with update interval from config)
 */
const initializeChartData = rawData => {
    let chartData = [];
    let currentIndex = 0;
    let nextReading = null;
    let currentChartSample = parseRawReading(rawData[currentIndex]);
    chartData.push(currentChartSample);
    currentIndex++;

    while (chartData.length < config.chart.dataLimit) {
        nextReading = parseRawReading(currentIndex);
        let currentTimeDifference = nextReading.x - currentChartSample.x;
        currentTimeDifference /= 1000;  // ms -> sec

        if (currentTimeDifference < config.chart.updateIntervalInSec){
            // Reading occurred faster than update interval
            // Need to include this reading and advance in raw reading data
            currentChartSample = nextReading;
            currentIndex++;
        }
        else {
            // Need to create new sample with same temperature as previously
            // But with added chart chart interval to time value
            currentChartSample = {
                x: new Date(
                    currentChartSample.x.getTime() + config.chart.updateIntervalInSec * 1000
                ),
                y: currentChartSample.y
            };
        }

        chartData.push(currentChartSample);
    }

    return List(chartData);
};

const parseRawReading = rawReading => ({
    x: new Date(rawReading.timestamp),
    y: rawReading.temperature
});

const updateChartData = (newPoint, oldData) => {
    const tempData = oldData.delete(0);

    return tempData.push(newPoint);
};

export const chartData = (state = initialState, action) => {
    switch (action.type) {
        case ActionTypes.CHART_INIT:
            return {
                isLoading: false,
                data: initializeChartData(action.rawData)
            };
        case ActionTypes.CHART_UPDATE:
            return {
                ...state,
                data: updateChartData(action.point, state.data)
            };
        default:
            return state;
    }
};
