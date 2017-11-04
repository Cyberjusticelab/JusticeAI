<style lang="scss" scoped>
@import "../theme/Landing"
</style>

<template>
    <el-container id="landing-component">
        <div id="landing-page">
            <div id="landing-page-nav">
                <el-row>
                    <el-col :md="4" :offset="20">
                        <el-button type="warning">Sign In</el-button>
                    </el-col>
                </el-row>
            </div>
            <div id="landing-page-title">
                <el-row>
                    <el-col :md="24">
                        <div id="title-image">
                            <img alt="" src="../assets/landing_page_zeus_avatar.png" id="landing-page-zeus">
                            <img alt="" src="../assets/logo.png" id="landing-page-logo">
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div id="landing-page-button-group">
                <el-row>
                    <el-col :md="24">
                        <div id="button-group">
                            <el-button type="warning" v-on:click="chooseType('tenant')">I am a tenant</el-button>
                            <el-button type="warning" v-on:click="chooseType('landlord')">I am a landlord</el-button>
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
        if (this.$localStorage.get('zeusId')) {
            this.$router.push('dashboard')
        }
    },
    methods: {
        chooseType(usertype) {
            this.$localStorage.set('username', usertype) //TODO: prompt username
            this.$localStorage.set('usertype', usertype)
            this.$localStorage.remove('zeusId')
            this.$router.push('dashboard')
        }
    }
}
</script>
