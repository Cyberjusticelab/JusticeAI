<style lang="scss" scoped>
@import "../theme/beta"
</style>

<template>
    <el-container id="beta-component">
        <div id="beta-page">
            <div id="about-us">
                <p>ABOUT US</p>
            </div>
            <div id="beta-page-title">
                <el-row>
                    <el-col :md="24">
                        <div id="title-image">
                            <img alt="" src="../assets/beta_page_zeus_avatar.png" id="beta-page-zeus">
                            <img alt="" src="../assets/beta_page_logo.png" id="beta-page-logo">
                        </div>
                    </el-col>
                    <el-col :md="24">
                        <div id="title-text">
                            <h2 id="beta_page_description">A conflict prevention tool that uses artificial intelligence and case data to answer questions from landlords and tenants regarding the likely outcome of a dispute.</h2>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div id="beta-page-button-group">
                <el-row>
                    <el-col :md="24">
                        <div id="button-group">
                            <el-button type="warning" v-on:click="chooseType('tenant')">SIGN UP TO BETA</el-button>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div id="beta-page-footer">
                <a href="http://www.cyberjustice.ca/" target="_blank">© 2017 Cyberjustice Laboratory</a>
            </div>
        </div>
    </el-container>
</template>

<script>
export default {
    created () {
    },
    methods: {
        chooseType(usertype) {
        }
    }
}
</script>
