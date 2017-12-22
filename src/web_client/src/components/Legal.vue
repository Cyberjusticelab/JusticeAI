<style lang="scss" scoped>
@import "../theme/Legal"
</style>

<template>
    <el-container id="legal-component">
        <el-row>
            <div id="legal-nav">
                <el-col :sm="6">
                    <div id="legal-nav-logo">
                        <img alt="" src="../assets/logo.png">
                    </div>
                </el-col>
                <el-col :sm="8" :offset="10">
                    <div id="legal-nav-item">
                        <p v-on:click="currentView='pp'" v-bind:class="{ 'active-view': currentView=='pp', 'hidden-view': currentView!=='pp'}">Privacy Policy</p>
                        <p v-on:click="currentView='eula'" v-bind:class="{ 'active-view': currentView=='eula', 'hidden-view': currentView!=='eula'}">End User License Agreement</p>
                        <a href="/">Home</a>
                    </div>
                </el-col>
            </div>
        </el-row>
        <div id="legal-content">
            <div v-if="currentView=='eula'">
                <el-row>
                    <el-col :sm="10" :offset="7">
                        <div class="legal-content-main-header">
                            <h1 v-html="eula.header"></h1>
                            <p v-html="eula.subheader"></p>
                        </div>
                    </el-col>
                </el-row>
                <div v-for="(section,index) in eula.content" v-bind:class="{ 'legal-content-body-1': index%2 !== 0, 'legal-content-body-2': index%2 == 0 }">
                    <el-row :gutter="24">
                        <el-col :sm="9" :offset="2">
                            <div class="legal-content-text">
                                <h4 v-html="section.title"></h4>
                                <p v-html="section.text"></p>
                            </div>
                        </el-col>
                        <el-col :sm="9" :offset="2">
                            <div class="legal-content-text">
                                <h4 v-html="section.subtitle"></h4>
                                <p v-html="section.summary">﻿</p>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </div>
            <div v-if="currentView=='pp'">
                <el-row>
                    <el-col :sm="10" :offset="7">
                        <div class="legal-content-main-header">
                            <h1 v-html="pp.header"></h1>
                            <p v-html="pp.subheader"></p>
                        </div>
                    </el-col>
                </el-row>
                <div v-for="(section,index) in pp.content" v-bind:class="{ 'legal-content-body-1': index%2 !== 0, 'legal-content-body-2': index%2 == 0 }">
                    <el-row :gutter="24">
                        <el-col :sm="4" :offset="4">
                            <div class="legal-content-text">
                                <h4 v-html="section.title"></h4>
                                <p v-html="section.text1"></p>
                            </div>
                        </el-col>
                        <el-col :sm="10" :offset="4">
                            <div class="legal-content-text">
                                <p v-html="section.text2"></p>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </div>         
        </div>
        <div id="legal-footer">
            <p>© 2017 Cyberjustice Laboratory</p>
        </div>
    </el-container>
</template>

<script>
export default {
    data () {
        return {
            api_url: process.env.API_URL,
            eula: new Object,
            pp: new Object,
            currentView: 'eula',
            connectionError: false
        }
    },
    created () {
        this.$http.get(this.api_url + 'legal').then(
            response => {
                for (let i = 0; i < response.body.length; i++) {
                    if (response.body[i].abbreviation === 'EULA') {
                        this.eula = response.body[i].html
                    }
                    if (response.body[i].abbreviation === 'PP') {
                        this.pp = response.body[i].html
                    }
                }
            },
            response => {
                this.connectionError = true
            }
        )
    }
}
</script>
