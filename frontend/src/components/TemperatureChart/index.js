import React, {Component} from 'react';
import {VictoryChart, VictoryAxis, VictoryLine, VictoryTooltip, VictoryVoronoiContainer} from 'victory';
import CircularProgress from '@material-ui/core/CircularProgress';

import './index.css';


class TemperatureChart extends Component {
    drawGridLines = y => {
        if (y === 30)
            return "#565550";

        if (y === 50)
            return "#265618";

        if (y === 60)
            return "#791415";
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
        if (this.props.isLoading)
            return (
                <div>
                    <CircularProgress />
                </div>
            );

        return (
            <div className="ChartArea">
                <VictoryChart
                    padding={{
                        left: 70,
                        right: 70,
                        top: 50,
                        bottom: 70
                    }}
                    containerComponent={<VictoryVoronoiContainer/>}
                    animate={{duration: 500}}
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
                        style={{
                            data: { stroke: "#b4b4b4" },
                        }}
                        labels={(d) => `Temperature: ${d.y}\nTime: ${d.x.toLocaleTimeString()}`}
                        labelComponent={<VictoryTooltip/>}
                        interpolation="stepBefore"
                        data={this.props.data}
                    />
                </VictoryChart>
            </div>
        )
    }
}


export default TemperatureChart;
