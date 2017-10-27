<style lang="scss" scoped>
@import "../theme/Legal"
</style>

<template>
    <b-container fluid id="legal-component">
        <div id="legal-nav">
            <b-row>
                <b-col md="3">
                    <div id="legal-nav-logo">
                        <img alt="" src="../assets/logo.png">
                    </div>
                </b-col>
                <b-col md="1" offset-md="8">
                    <div id="legal-nav-item">
                        <a href="/">Home</a>
                    </div>
                </b-col>
            </b-row>
        </div>
        <div id="legal-content">
            <b-row>
                <b-col md="6" offset-md="3">
                    <div class="legal-content-main-header">
                        <h1>{{ eula.header }}</h1>
                        <p>{{ eula.subheader }} </p>
                    </div>
                </b-col>
            </b-row>
            <div v-for="(section,index) in eula.content" v-bind:class="{ 'legal-content-body-1': index%2 !== 0, 'legal-content-body-2': index%2 == 0 }">
                <b-row>
                    <b-col md="5" offset-md="1">
                        <div class="legal-content-text">
                            <h4>{{ section.title }}</h4>
                            <p>{{ section.text }}</p>
                        </div>
                    </b-col>
                    <b-col md="5">
                        <div class="legal-content-text">
                            <h4>{{ section.subtitle }}</h4>
                            <p>﻿{{ section.summary }}</p>
                        </div>
                    </b-col>
                </b-row>
            </div>
        </div>
        <div id="legal-footer">
            <b-row>
                <b-col md="4" offset="1">
                    <p>© 2017 Cyberjustice Laboratory</p>
                </b-col>
            </b-row>
        </div>
    </b-container>
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
