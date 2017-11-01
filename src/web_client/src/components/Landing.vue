<style lang="scss" scoped>
@import "../theme/Landing"
</style>

<template>
    <b-container fluid id="landing-component">
        <div id="landing-page">
            <div id="landing-page-nav">
                <b-row>
                    <b-col md="1" offset-md="11">
                        <b-button size="sm" variant="warning">Sign In</b-button>
                    </b-col>
                </b-row>
            </div>
            <div id="landing-page-title">
                <b-row>
                    <b-col md="4" offset="4">
                        <div id="title-image">
                            <img alt="" src="../assets/landing_page_zeus_avatar.png" id="landing-page-zeus">
                            <img alt="" src="../assets/logo.png" id="landing-page-logo">
                        </div>
                    </b-col>
                </b-row>
            </div>
            <div id="landing-page-button-group">
                <b-row>
                    <b-col md="6" offset="3">
                        <div id="button-group">
                            <b-button size="lg" variant="outline-success" v-on:click="chooseType('tenant')">I am a tenant</b-button>
                            <b-button size="lg" variant="outline-success" v-on:click="chooseType('landlord')">I am a landlord</b-button>
                        </div>
                    </b-col>
                </b-row>
            </div>
        </div>
    </b-container>
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
            this.$localStorage.set('usertype', usertype)
            this.$localStorage.remove('zeusId')
            this.$router.push('dashboard')
        }
    }
}
</script>
