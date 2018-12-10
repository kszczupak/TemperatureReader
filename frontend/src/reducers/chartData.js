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
    // console.log(JSON.stringify(rawData));
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
        console.log(currentTimeDifference);

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

    console.log(`Last index: ${currentIndex}`);

    return List(chartData.reverse());
};

const parseRawReading = rawReading => ({
    x: new Date(rawReading.timestamp * 1000),
    y: rawReading.temperature
});

const updateChartData = (newPoint, oldData) => {
    const tempData = oldData.delete(0);

    // console.log(tempData.push(newPoint).toJS());

    return tempData.push(newPoint);
};

const debugChartData = JSON.parse("[{\"timestamp\":1544469009.900121,\"temperature\":28},{\"timestamp\":1544469307.283505,\"temperature\":27},{\"timestamp\":1544469417.371111,\"temperature\":28},{\"timestamp\":1544469507.630034,\"temperature\":29},{\"timestamp\":1544469537.701864,\"temperature\":30},{\"timestamp\":1544469557.646464,\"temperature\":31},{\"timestamp\":1544469577.794979,\"temperature\":32},{\"timestamp\":1544469587.741643,\"temperature\":33},{\"timestamp\":1544469607.683816,\"temperature\":34},{\"timestamp\":1544469627.860231,\"temperature\":35},{\"timestamp\":1544469647.840578,\"temperature\":36},{\"timestamp\":1544469667.881888,\"temperature\":37},{\"timestamp\":1544469708.04574,\"temperature\":38},{\"timestamp\":1544469820.271771,\"temperature\":37},{\"timestamp\":1544470038.526727,\"temperature\":38},{\"timestamp\":1544470118.664155,\"temperature\":39},{\"timestamp\":1544470178.765871,\"temperature\":40},{\"timestamp\":1544470248.988271,\"temperature\":41},{\"timestamp\":1544470318.985788,\"temperature\":42},{\"timestamp\":1544470789.891962,\"temperature\":41}]");

export const chartData = (state = initialState, action) => {
    switch (action.type) {
        case ActionTypes.CHART_DEBUG:
            return {
                isLoading: false,
                data: initializeChartData(debugChartData)
            };
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
