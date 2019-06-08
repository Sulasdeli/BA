import React, {Component} from 'react'
import {Highcharts3dChart, withHighcharts, XAxis, YAxis, ZAxis, Tooltip, ScatterSeries, Scatter3dSeries}
    from 'react-jsx-highcharts'
import Highcharts from 'highcharts';
import {Button, Slider} from 'rsuite';
import addHighcharts3DModule from 'highcharts/highcharts-3d';
import styled from "styled-components";
import {Card} from "@material-ui/core";
import CardHeader from "./CardHeader";
addHighcharts3DModule(Highcharts);

const ChartContainer = styled.div`
  margin-bottom: 45px;
`;

const SettingsContainer = styled.div`
  padding:15px;
  margin-top: -20px;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
`;

const pointFormatter = function()  {
    return `<strong>${this.series.name}</strong><br/>Deployment Time: ${this.point.x}<br />Leasing Period:
            ${this.point.y}<br />Budget: ${this.point.z}`
};

class IndexPlot extends Component {
    constructor() {
        super();
        this.state = {
            beta: 22,
            alpha: 20
        };
    }

    handleSliderChange = (e, name) => {
        this.setState({
            [name]: e
        });
    };

    render() {
        return (
            <ChartContainer>
                <Card style={{borderRadius: "10px"}}>
                    <CardHeader iconName={"line-chart"} title='Plot' backgroundColor='linear-gradient(0deg, #66bb6a, #43a047)'/>
                    <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
                        <Highcharts3dChart alpha={this.state.alpha} beta={this.state.beta} depth="300" legend={{enabled: true}}>
                            <Tooltip formatter={pointFormatter}/>
                            <XAxis min={0}>
                                <XAxis.Title style={{fontWeight: "bold", fontSize: 15}} margin={40}>Deployment Time</XAxis.Title>
                            </XAxis>
                            <YAxis min={0}>
                                <YAxis.Title style={{fontWeight: "bold", fontSize: 15}} margin={40}>Leasing Period</YAxis.Title>
                            </YAxis>
                            <ZAxis min={0}>
                                <ZAxis.Title style={{fontWeight: "bold", fontSize: 15}} margin={-400}>Budget</ZAxis.Title>
                                <Scatter3dSeries name="User Profile Index" color={"red"} lineWidth={2} data={[[0,0,0], this.props.userIndex]}/>
                                {this.props.services.map((s, i) => <ScatterSeries key={i} lineWidth={1} name={s.providerName} data={[[0,0,0], JSON.parse(s.weightedSimilarity)]}/>)}
                            </ZAxis>
                        </Highcharts3dChart>
                    </div>
                    <hr/>
                    <SettingsContainer>
                        <div>
                            <h6 style={{fontWeight: 'bold', fontSize: 16}}>Beta Angle</h6>
                            <Slider style={{ width: 250 }} value={this.state.beta} onChange={(e) => this.handleSliderChange(e, "beta")}/>
                        </div>
                        <div>
                            <h6 style={{fontWeight: 'bold', fontSize: 16}}>Alpha Angle</h6>
                            <Slider style={{ width: 250 }} value={this.state.alpha} onChange={(e) => this.handleSliderChange(e, "alpha")}/>
                        </div>
                    </SettingsContainer>
                    <Button color="blue" appearance="ghost" onClick={() => this.setState({beta: 22, alpha: 20})}>Reset</Button>
                </Card>
            </ChartContainer>
        );
    }
}

export default withHighcharts(IndexPlot, Highcharts);
