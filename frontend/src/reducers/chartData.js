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
    // let currentIndex = config.chart.dataLimit;
    let currentIndex = rawData.length - 1;
    let previousReading = null;
    // rawData.reverse();  // Reverse to obtain most recent samples

    let currentChartSample = parseRawReading(rawData[currentIndex]);
    currentChartSample = {
        ...currentChartSample,
        x: new Date()
    };
    chartData.push(currentChartSample);
    currentIndex--;

    while (chartData.length < config.chart.dataLimit && currentIndex >= 0) {
        previousReading = parseRawReading(rawData[currentIndex]);
        let currentTimeDifference = currentChartSample.x - previousReading.x;
        currentTimeDifference /= 1000;  // ms -> sec

        if (currentTimeDifference < config.chart.updateIntervalInSec){
            // Reading occurred faster than update interval
            // Need to include this reading and advance in raw reading data
            currentChartSample = previousReading;
            currentIndex--;
        }
        else {
            // Need to create new sample with same temperature as previously
            // But with added chart chart interval to time value
            currentChartSample = {
                ...currentChartSample,
                x: new Date(
                    currentChartSample.x.getTime() - config.chart.updateIntervalInSec * 1000
                )
            };
        }

        chartData.push(currentChartSample);
    }

    return List(chartData.reverse());
};

const parseRawReading = rawReading => ({
    x: new Date(rawReading.timestamp * 1000),
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
