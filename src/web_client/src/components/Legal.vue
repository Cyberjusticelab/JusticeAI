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
                <el-col :sm="2" :offset="16">
                    <div id="legal-nav-item">
                        <a href="/">Home</a>
                    </div>
                </el-col>
            </div>
        </el-row>
        <div id="legal-content">
            <el-row>
                <el-col :sm="12" :offset="6">
                    <div class="legal-content-main-header">
                        <h1>{{ eula.header }}</h1>
                        <p>{{ eula.subheader }} </p>
                    </div>
                </el-col>
            </el-row>
            <div v-for="(section,index) in eula.content" v-bind:class="{ 'legal-content-body-1': index%2 !== 0, 'legal-content-body-2': index%2 == 0 }">
                <el-row :gutter="24">
                    <el-col :sm="12">
                        <div class="legal-content-text">
                            <h4>{{ section.title }}</h4>
                            <p>{{ section.text }}</p>
                        </div>
                    </el-col>
                    <el-col :sm="12">
                        <div class="legal-content-text">
                            <h4>{{ section.subtitle }}</h4>
                            <p>﻿{{ section.summary }}</p>
                        </div>
                    </el-col>
                </el-row>
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
            connectionError: false
        }
    },
    created () {
        this.$http.get(this.api_url + 'legal').then(
            response => {
                this.eula = response.body[0].html
            },
            response => {
                this.connectionError = true
            }
        )
    }
}
</script>
