<style lang="scss" scoped>
@import "../theme/beta"
</style>

<template>
    <el-container id="beta-component">
        <div id="beta-page">
            <div id="beta-page-title">
                <el-row>
                    <el-col :md="24">
                        <div id="title-image">
                            <img alt="" src="../assets/beta_page_zeus_avatar.png" id="beta-page-zeus">
                            <img alt="" src="../assets/beta_page_logo.png" id="beta-page-logo">
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
