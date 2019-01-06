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
    let readingIndex = rawData.length - 1;
    let currentReading = parseRawReading(rawData[readingIndex]);

    // First chart sample will contain last temperature value and current time
    let currentChartSample = {
        ...currentReading,
        x: new Date()
    };
    chartData.push(currentChartSample);

    // This loop will build chart data (in reverse order)
    // If samples interval (from config) is less than time between consecutive reading,
    // readings will be filled with same temperature value.
    while (chartData.length < config.chart.dataLimit) {
        let samplesTimeDifference = currentChartSample.x - currentReading.x;
        samplesTimeDifference /= 1000;  // ms -> sec

        if (samplesTimeDifference < config.chart.updateIntervalInSec) {
            // Reading occurred faster than update interval
            // Need to include this reading and advance in raw reading data
            currentChartSample = currentReading;    // Take event time from reading
            readingIndex--;                         // Advance in reading data
            if (readingIndex < 0) break;
            currentReading = parseRawReading(rawData[readingIndex]);
            currentChartSample = {
                ...currentChartSample,
                y: currentReading.y                 // Take temperature from next reading
            };
        } else {
            // Need to create new sample with same temperature as previously
            // But with subtracted chart chart interval to time value
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
    let tempData = oldData;
    if (oldData.length >= config.chart.dataLimit) tempData = oldData.delete(0);

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
