<style lang="scss" scoped>
@import "../theme/Sidebar"
</style>

<template>
    <div id="sidebar-component" v-bind:class="{ 'burger-menu': !openSidebar }">
        <!-- 1. Menu Close -->
        <div v-if="!openSidebar" v-on:click="view()" id="sidebar-min">
            <img alt="" src="../assets/sidebar-toggle.png">
        </div>
        <!-- 1. End of Menu Close -->
        <!-- 2.1 Menu Open -->
        <transition name="translate">
            <div v-if="openSidebar && !isPredicted" id="sidebar-full">
                <!-- LOGO -->
                <div id="sidebar-logo">
                    <img alt="" src="../assets/logo.png">
                    <p>Beta</p>
                </div>
                <!-- End of LOGO -->
                <!-- Pending Info -->
                <div id="sidebar-info">
                    <el-progress type="circle" :percentage="progress"></el-progress>
                    <p>Provide more information to Zeus to get a prediction on your case</p>
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
        <!-- 2.1 End of Menu Open -->
        <!-- 2.2 Stat Dashboard -->
        <transition name="el-zoom-in-center">
            <div v-if="openSidebar && isPredicted" id="sidebar-dashboard">
                <el-row>
                    <el-col :sm="{span: 24, offset: 0}">
                        <div id="sidebar-dashboard-logo">
                            <img alt="" src="../assets/logo.png">
                        </div>
                    </el-col>
                    <el-col :sm="{span: 1, offset: 23}">
                        <img id="sidebar-dashboard-close" v-on:click="openSidebar = false" alt="" src="../assets/history_disable.png">
                    </el-col>
                    <el-col :sm="{span: 24, offset: 0}">
                        <div id="sidebar-dashboard-header">
                            <h2>Here is our prediction after analyzing <span>{{ report.data_set }}</span> Régie du logement"s precedents:</h2>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 5, offset: 2}">
                        <div id="sidebar-dashboard-accuracy">
                            <el-progress type="circle" :percentage="report.accuracy" :stroke-width="30" :width="250"></el-progress>
                            <h3>Prediction Accuracy</h3>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 8, offset: 2}">
                        <div id="sidebar-dashboard-curve">
                            <el-carousel indicator-position="outside">
                                <div v-for="value,key in report.curves">
                                    <el-carousel-item :key="key" :name="key">
                                        <vue-chart
                                            type="bar"
                                            :data="chartData"
                                            :options="{scales: {yAxes: [{ticks: {beginAtZero: true}}]}}"
                                            :update-config="{duration: 800, easing: 'easeOutBounce'}"
                                        ></vue-chart>
                                        properties
                                    </el-carousel-item>
                                </div>
                            </el-carousel>
                            <h3>Payment Verdict</h3>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 4, offset: 2}">
                        <div id="sidebar-dashboard-outcome">
                            <h2>Case Verdict</h2>
                            <div v-for="value,key in report.outcomes" class="sidebar-dashboard-outcome-item">
                                <el-col :sm="{span: 20, offset: 0}">
                                    <h3>{{ key }}</h3>
                                </el-col>
                                <el-col :sm="{span: 2, offset: 2}">
                                    <icon name="check-square" class="outcome-check"></icon>
                                </el-col>
                            </div>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 22, offset: 1}">
                        <div id="sidebar-dashboard-similarity">
                                <el-table :data="report.similar_precedents_table" stripe>
                                    <div>
                                        <el-table-column prop="name" label="Case Number"></el-table-column>
                                    </div>
                                    <div v-for="fact in report.similar_precedents_fact_index">
                                        <el-table-column :prop="fact" :label="fact"></el-table-column>
                                    </div>
                                    <div v-for="outcome in report.similar_precedents_outcome_index">
                                        <el-table-column :prop="outcome" :label="outcome"></el-table-column>
                                    </div>
                                </el-table>
                        </div>
                    </el-col>
                    <el-col :sm="{span: 22, offset: 1}">
                        <div id="sidebar-dashboard-contact">
                            <h3>Need professional legal support? Contact us at 514-123-4567</h3>
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
        <!-- 2.2 End of Stat Dashboard -->
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
export default {
    data () {
        return {
            openFeedbackModal: false,
            openSidebar: false,
            isPredicted: false,
            username: this.$localStorage.get('username'),
            usertype: this.$localStorage.get('usertype'),
            feedback: '',
            progress: 0,
            //TODO: set report to new object and modify by report api callback. Now mock data.
            //This is the expected payload format
            report: {
                accuracy: 90,
                data_set: 350000,
                similar_case: 50,
                curves: {
                    legal_fees: ['whatever data is needed to create a bell curve'],
                    additional_indemnity_fees: ['whatever data is needed to create a bell curve']
                },
                outcomes: {
                    lease_termination: 1,
                    order_resiliation: 1,
                    apartment_impropre: 1,
                    legal_fees: 82,
                    additional_indemnity_fees: 1000
                },
                similar_precedents: [
                    {
                        precedent: 'AZ-1111111',
                        facts: {
                            f1: 1,
                            f2: 1,
                            f3: 1,
                            f4: 1,
                            f5: 1
                        },
                        outcomes: {
                            o1: 1,
                            o2: 1,
                            o3: 1
                        }
                    },
                    {
                        precedent: 'AZ-222222',
                        facts: {
                            f1: 0,
                            f2: 0,
                            f3: 0,
                            f4: 0,
                            f5: 1
                        },
                        outcomes: {
                            o1: 0,
                            o2: 0,
                            o3: 1
                        }
                    }
                ]
            },
            api_url: process.env.API_URL,
            connectionError: false
        }
    },
    created () {
        EventBus.$on('hideSidebar', (status) => {
            this.openSidebar = false
            this.progress = status.progress
            this.isPredicted = status.prediction
        })
    },
    methods: {
        view () {
            // TODO: do some black magic here to call report endpoint
            this.openSidebar = true
            //this.isPredicted = true // TODO: remove this dev code. change to true for testing dashboard UI
            if (this.isPredicted) {
                //TODO:
                this.createPrecedentTable()
            }
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
        resetChat () {
            this.$localStorage.remove('zeusId')
            this.$localStorage.remove('username')
            this.$localStorage.remove('usertype')
            this.$router.push('/')
        },
        createPrecedentTable () {
            this.report.similar_precedents_fact_index = []
            for (let key in this.report.similar_precedents[0].facts) {
                this.report.similar_precedents_fact_index.push(key)
            }
            this.report.similar_precedents_outcome_index = []
            for (let key in this.report.similar_precedents[0].outcomes) {
                this.report.similar_precedents_outcome_index.push(key)
            }
            this.report.similar_precedents_table = []
            for (let i = 0; i < this.report.similar_precedents.length; i++) {
                let row = {}
                row.name = this.report.similar_precedents[i].precedent
                for (let key in this.report.similar_precedents[i].facts) {
                    row[key] = this.report.similar_precedents[i].facts[key]
                }
                for (let key in this.report.similar_precedents[i].outcomes) {
                    row[key] = this.report.similar_precedents[i].outcomes[key]
                }
                this.report.similar_precedents_table.push(row)
            }
        }
    }
}
</script>
