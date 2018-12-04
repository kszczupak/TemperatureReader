import React, {Component} from 'react';
import {PropTypes} from 'prop-types';
import {VictoryBar, VictoryChart, VictoryAxis, VictoryTheme, VictoryStack, VictoryLine} from 'victory';

import './index.css';


class TemperatureChart extends Component {
    drawGridLines = y => {
        if (y === 50)
            return "#265618";

        if (y === 60)
            return "#561314";
    };

    getTickValues = () => {
        if (this.props.data.length < 2)
            return new Date();

        const firstTick = this.props.data[0].x;
        const lastTick = this.props.data[this.props.data.length - 1].x;

        return [firstTick, lastTick];
    };

    componentDidMount() {
        this.props.startPeriodicChartUpdates();
    }

    componentWillUnmount() {
        this.props.stopPeriodicChartUpdates();
    }

    render() {
        console.log(this.props.data);

        return (
            <div className="ChartArea">
                <VictoryChart
                    padding={{
                        left: 70,
                        right: 70,
                        top: 50,
                        bottom: 70
                    }}
                >
                    <VictoryAxis
                        style={{
                            axis: {stroke: "#ffffff"},
                            axisLabel: {
                                fill: "#ffffff",
                                fontSize: 20,
                                padding: 40
                            },
                            tickLabels: {fill: "#ffffff"}
                        }}
                        tickValues={this.getTickValues()}
                        tickFormat={x => {
                            if (x instanceof Date || x instanceof Array)
                                return x.toLocaleTimeString();
                        }}
                        label="Time"
                    />
                    <VictoryAxis
                        dependentAxis
                        domain={[20, 65]}
                        style={{
                            axis: {stroke: "#ffffff"},
                            axisLabel: {
                                fill: "#ffffff",
                                fontSize: 20,
                                padding: 40
                            },
                            tickLabels: {fill: "#ffffff"},
                            grid: {
                                stroke: this.drawGridLines,
                                strokeDasharray: "7, 5"
                            }
                        }}
                        label="Temperature"
                    />
                    <VictoryLine
                        data={this.props.data}
                    />
                </VictoryChart>
            </div>
        )
    }
}

TemperatureChart.propTypes = {
    // monitor: PropTypes.object.isRequired,
};

export default TemperatureChart;
