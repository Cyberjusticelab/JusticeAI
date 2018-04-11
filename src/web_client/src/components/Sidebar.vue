<style lang="scss" scoped>
@import "../theme/Sidebar"
</style>

<template>
    <div id="sidebar-component">
        <!-- 1. Default Sidebar -->
        <transition name="translate">
            <div v-if="!openDashboard" id="sidebar-full">
                <!-- LOGO -->
                <div id="sidebar-logo">
                    <img alt="" src="../assets/logo.png">
                    <p>Beta</p>
                </div>
                <!-- End of LOGO -->
                <!-- Pending Info -->
                <div id="sidebar-info">
                    <el-progress type="circle" :percentage="progress"></el-progress>
                    <p v-if="progress < 100">Provide more information to Zeus to get a prediction on your case</p>
                    <h2 v-if="isPredicted" v-on:click="openDashboard = true">See Latest Prediction</h2>
                </div>
                <!-- End of Pending Info -->
                <!-- Feedback -->
                <div v-on:click="openFeedbackModal = true" class="sidebar-option">
                    <p>FEEDBACK</p>
                </div>
                <!-- End of Feedback -->
                <!-- Reset -->
                <div v-on:click="resetChat()" class="sidebar-option">
                    <p>RESET CONVERSATION</p>
                </div>
                <!-- End of Reset -->
            </div>
        </transition>
        <!-- 1. End of Default Sidebar -->
        <!-- 2. Stat Dashboard -->
        <transition name="el-zoom-in-center">
            <div v-show="openDashboard" id="sidebar-dashboard">
                <el-row>
                    <el-col :sm="{span: 24, offset: 0}">
                        <div id="sidebar-dashboard-logo">
                            <img alt="" src="../assets/logo.png">
                        </div>
                    </el-col>
                    <el-col :sm="{span: 1, offset: 23}">
                        <img id="sidebar-dashboard-close" v-on:click="openDashboard = false" alt="" src="../assets/history_disable.png">
                    </el-col>
                    <el-col :sm="{span: 24, offset: 0}">
                        <div id="sidebar-dashboard-header">
                            <h2>Here is our prediction after analyzing <span>{{ report.data_set }}</span> Régie du logement's precedents:</h2>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 5, offset: 1}">
                        <div id="sidebar-dashboard-accuracy">
                            <el-progress type="circle" :percentage="report.accuracy" :stroke-width="30" :width="250"></el-progress>
                            <h3>Prediction Probability</h3>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 8, offset: 2}">
                        <div id="sidebar-dashboard-curve">
                            <el-carousel indicator-position="outside">
                                <div v-for="value,key in report.curves">
                                  <el-carousel-item :key="key" :name="key">
                                      <div class="bellcurve" ref="bellcurve"></div>
                                  </el-carousel-item>
                                </div>
                                <h1 v-show="!hasGraph">This functionality is not available for this prediction</h1>
                            </el-carousel>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 5, offset: 2}">
                        <div id="sidebar-dashboard-outcome">
                            <h2>Case Verdict</h2>
                            <div v-for="value,key in report.outcomes" class="sidebar-dashboard-outcome-item">
                                <el-col :sm="{span: 20, offset: 0}">
                                    <h3>{{ key }}</h3>
                                </el-col>
                                <el-col :sm="{span: 2, offset: 2}">
                                    <icon name="check-square" class="outcome-check" v-if="value == true"></icon>
                                    <icon name="window-close" class="outcome-check" v-if="value == false"></icon>
                                    <h3 v-if="value !== true && value !== false">{{ value}}</h3>
                                </el-col>
                            </div>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 22, offset: 1}">
                        <div id="sidebar-dashboard-similarity">
                                <h3>Here are <span>{{ report.similar_case }}</span> most similar precendents to your case</h3>
                                <el-table :data="report.precedent_table" @header-click="openSimilarPrecedent" stripe>
                                    <div>
                                        <el-table-column prop="name" align="center" fixed="left"></el-table-column>
                                    </div>
                                    <div v-for="header in report.precedent_table_header">
                                        <el-table-column :prop="header" :label="header" label-class-name="precedent-table-header" align="center"></el-table-column>
                                    </div>
                                </el-table>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 22, offset: 1}">
                        <div id="sidebar-dashboard-contact">
                            <h3>Need professional legal support? Contact us at 555-555-5555</h3>
                            <div v-on:click="openFeedbackModal = true" class="sidebar-dashboard-footer">
                                <p>FEEDBACK</p>
                            </div>
                            <!-- End of Feedback -->
                            <!-- Reset -->
                            <div v-on:click="resetChat()" class="sidebar-dashboard-footer">
                                <p>RESET CONVERSATION</p>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </transition>
        <!-- 2. End of Stat Dashboard -->
        <!-- el-dialog for feedback -->
        <el-dialog title="Feedback" :visible.sync="openFeedbackModal">
            <textarea id="feedback-input" v-model="feedback">
            </textarea>
            <span slot="footer" class="dialog-footer">
                <el-button v-on:click="openFeedbackModal = false">Cancel</el-button>
                <el-button type="primary" v-on:click="submitFeedback()">Submit</el-button>
            </span>
        </el-dialog>
        <!-- End of el-dialog for feedback -->
    </div>
</template>

<script>
import { EventBus } from './EventBus.js'
import * as d3 from "d3";
export default {
    data () {
        return {
            openFeedbackModal: false,
            openDashboard: false,
            isPredicted: false,
            hasGraph: false,
            feedback: '',
            progress: 0,
            report: new Object,
            api_url: process.env.API_URL,
            connectionError: false
        }
    },
    created () {
        // resume progress bar
        this.progress = parseInt(this.$localStorage.get('progress')) | 0
        if (this.progress > 100) {
            this.progress = 100
        }
        // resume dashboard
        if (this.$localStorage.get('isPredicted')) {
            this.view()
        }
        // capture event to set progress bar and update dashboard
        EventBus.$on('updateSidebar', () => {
            this.progress = parseInt(this.$localStorage.get('progress'))
            if (this.progress > 100) {
                this.progress = 100
            }
            if (this.progress == 100) {
                this.view()
            }
        })
    },
    methods: {
        view () {
            let zeusId = this.$localStorage.get('zeusId')
            this.$http.get(this.api_url + 'conversation/' + zeusId + '/report').then(
                response => {
                    this.report = response.body.report
                    this.report.accuracy = parseFloat((this.report.accuracy * 100).toFixed(2))
                    this.createPrecedentTable()
                    this.isPredicted = true
                    this.$localStorage.set('isPredicted', true)
                    // D3 chart required manual DOM manipulation
                    // SetTimeout to wait until Vue renders it
                    if (Object.keys(this.report.curves).length > 0) {
                        setTimeout(() => {
                            this.hasGraph = true
                            this.createBellCurves()
                        }, 50);
                    }
                },
                response => {
                    console.log('Connection Fail: get report')
                    this.connectionError = true
                }
            )
        },
        submitFeedback () {
            if (this.feedback) {
                this.$http.post(this.api_url + 'feedback',{
                    feedback: this.feedback
                }).then(
                    response => {
                        alert('Thank you for providing us with feedback!');
                        this.openFeedbackModal = false;
                        this.feedback = '';
                    },
                    response => {
                        this.connectionError = true
                        alert('Sorry, an error occurred and we could not receive your feedback.');
                        this.openFeedbackModal = false;
                        this.feedback = '';
                    }
                )
            } else {
                alert('No feedback entered');
            }
        },
        createPrecedentTable () {
            // create user case data vector
            let zeusId = this.$localStorage.get('zeusId')
            this.$http.get(this.api_url + 'conversation/' + zeusId + '/resolved').then(
                response => {
                    // prep the precedent table
                    let precedent_table = []
                    // append user case outcomes
                    let user_data = {}
                    for (let key in this.report.outcomes) {
                        user_data[key] = this.report.outcomes[key]
                    }
                    // append user case facts
                    for (let i = 0; i < response.body.fact_entities.length; i++) {
                        user_data[response.body.fact_entities[i].fact.name] = response.body.fact_entities[i].value
                    }
                    // extract data from similar precedent as fact vector
                    for (let key in this.report.similar_precedents[0].facts) {
                        let fact_vector = {}
                        fact_vector.name = key
                        for (let i = 0; i < this.report.similar_precedents.length; i++) {
                            fact_vector[this.report.similar_precedents[i].precedent] = this.report.similar_precedents[i].facts[key]
                        }
                        precedent_table.push(fact_vector)
                    }
                    // extract data from similar precedent as fact vector
                    for (let key in this.report.similar_precedents[0].outcomes) {
                        let outcome_vector = {}
                        outcome_vector.name = key
                        for (let i = 0; i < this.report.similar_precedents.length; i++) {
                            outcome_vector[this.report.similar_precedents[i].precedent] = this.report.similar_precedents[i].outcomes[key]
                        }
                        precedent_table.push(outcome_vector)
                    }
                    // add all user data to the table and format the table
                    for (let i = 0; i < precedent_table.length; i++) {
                        precedent_table[i]['Your Case'] = user_data[precedent_table[i].name]
                        for (let key in precedent_table[i]) {
                            if (typeof precedent_table[i][key] !== 'string') {
                                precedent_table[i][key] = precedent_table[i][key].toString()
                            }
                        }
                    }
                    // create header list
                    let header_list = ['Your Case']
                    for (let key in precedent_table[0]) {
                        if (key !== 'name' && key !== 'Your Case') {
                            header_list.push(key)
                        }
                    }
                    // settle the table data
                    this.report.precedent_table_header = header_list
                    this.report.precedent_table = precedent_table
                },
                response => {
                    this.connectionError = true
                    console.log("Connection Fail: get user resolved fact")
                }
            )
        },
        openSimilarPrecedent (column,event) {
            if (column.label !== 'Your Case'){
                window.open("https://www.rdl2.gouv.qc.ca/internet/asp/consultation-dossier/DossierDetail.asp?dossier=" + column.label, '_blank')
            }
        },
        resetChat () {
            this.$localStorage.remove('zeusId')
            this.$localStorage.remove('username')
            this.$localStorage.remove('usertype')
            this.$localStorage.remove('progress')
            this.$localStorage.remove('isPredicted')
            this.$router.push('/')
        },
        createBellCurves() {
            // Data common to all normal distributions
            const NUMBER_OF_DECIMALS_REPORTED = 2
            let MARGIN_SIZE = 20;
            let width = 450 - (2 * MARGIN_SIZE);
            let height = 275 - (2 * MARGIN_SIZE);
            let x = d3.scale.linear().range([0, width]);
            let y = d3.scale.linear().range([height, 0]);

            // Data specific to each normal distribution
            let self = this;
            Object.keys(this.report.curves).forEach(function(ranged_outcome, i) {
                // Obtaine values from report
                let mean = self.report.curves[ranged_outcome].mean;
                let standardDeviation = self.report.curves[ranged_outcome].std;
                let value = self.report.curves[ranged_outcome].outcome_value;

                // Show values and legend above chart
                // Styling must be applied here due to dynamic DOM node creation
                d3.select(self.$refs.bellcurve[i]).insert("div")[0][0].innerHTML = ranged_outcome + "<br/>" +
                    "<span style='color: green;'>mean</span>: " +  mean.toFixed(NUMBER_OF_DECIMALS_REPORTED) +
                    " <span style='color: steelblue;'>std</span>: " + standardDeviation.toFixed(NUMBER_OF_DECIMALS_REPORTED) +
                    " <span style='color: red;'>value</span>: " + value.toFixed(NUMBER_OF_DECIMALS_REPORTED);

                // Create chart
                let svg = d3.select(self.$refs.bellcurve[i]).append("svg")
                    .attr("width", width + (2 * MARGIN_SIZE))
                    .attr("height", height + (2 * MARGIN_SIZE))
                    .append("g")
                    .attr("transform", "translate(" + MARGIN_SIZE + "," + MARGIN_SIZE + ")");

                // Create standardized normal distribution data
                let data = self._generateBellCurveData(0, standardDeviation / mean);
                let verticalValueData = self._generateBellCurveVerticalData((value - mean)/standardDeviation);
                let verticalMeanData = self._generateBellCurveVerticalData(0);
                let verticalLine = _createD3Line();
                let bell_line = _createD3Line();

                // Fit chart size to data
                x.domain(d3.extent(data, function(d) {
                    return d.q;
                }));
                y.domain(d3.extent(data, function(d) {
                    return d.p;
                }));

                // Generate lines based on data sets
                svg.append("path")
                    .datum(data)
                    .attr("d", bell_line)
                    .style("fill", "none")
                    .style("stroke", "steelblue")
                    .style("stroke-width", "2px");

                svg.append("path")
                    .datum(verticalValueData)
                    .attr("d", verticalLine)
                    .style("fill", "none")
                    .style("stroke", "red")
                    .style("stroke-width", "1px");

                svg.append("path")
                    .datum(verticalMeanData)
                    .attr("d", verticalLine)
                    .style("fill", "none")
                    .style("stroke", "green")
                    .style("stroke-width", "1px");
            });

            function _createD3Line() {
                return d3.svg.line()
                    .x(function(d) {
                        return x(d.q);
                    })
                    .y(function(d) {
                        return y(d.p);
                    });
            }

        },
        _generateBellCurveVerticalData (value) {
            return [
                {
                    "q": value,
                    "p": 0
                },
                {
                    "q": value,
                    "p": 1
                }
            ]
        },
        _generateBellCurveData (mean, standardDeviation) {
            let temp_data = []
            for (let i = 0; i < 10000; i++) {
                let q = this._bellCurveNormal()
                let p = this._bellCurveGaussian(mean, standardDeviation, q)
                // probability - quantile pairs
                let el = {
                    "q": q,
                    "p": p
                }
                temp_data.push(el)
            };

            return temp_data.sort(function(x, y) {
                return x.q - y.q;
            });
        },
        _bellCurveNormal () {
            let x = 0;
            let y = 0;
            let rds;
            let c;
            do {
                x = Math.random() * 2 - 1;
                y = Math.random() * 2 - 1;
                rds = x * x + y * y;
            } while (rds == 0 || rds > 1);
            c = Math.sqrt(-2 * Math.log(rds) / rds); // Box-Muller transform
            return x * c; // throw away extra sample y * c
        },
        _bellCurveGaussian (mean, sigma, x) {
            let gaussianConstant = 1 / Math.sqrt(2 * Math.PI);
            x = (x - mean) / sigma;
            return gaussianConstant * Math.exp(-.5 * x * x) / sigma;
        }
    }
}
</script>

<style type="text/css">
.precedent-table-header {
    font-weight: bold;
    font-size: 18px;
    color: #5D5E5E;
}
.precedent-table-header:hover {
    color: #E9A742;
    cursor: pointer;
}
</style>

