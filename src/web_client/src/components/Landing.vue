<style lang="scss" scoped>
@import "../theme/Landing"
</style>

<template>
    <el-container id="landing-component">
        <div id="landing-page">
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
            <!-- el-dialog for username -->
            <el-dialog :visible.sync="promptUsername" center>
                <h2>PLEASE ENTER YOUR NAME</h2>
                <el-input v-model="username" placeholder="ENTER YOUR NAME"></el-input>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" v-on:click="login()" v-if="username">Next</el-button>
                    <el-button type="primary" v-on:click="login()" v-if="!username">Skip</el-button>
                    <el-button v-on:click="promptUsername = false">Cancel</el-button>
                </span>
            </el-dialog>
            <!-- End of el-dialog for username -->
        </div>
    </el-container>
</template>

<script>
export default {
    data () {
        return {
            promptUsername: false,
            username: null
        }
    },
    created () {
        if (this.$localStorage.get('zeusId')) {
            this.$router.push('dashboard')
        }
    },
    methods: {
        chooseType(usertype) {
            this.$localStorage.set('usertype', usertype)
            this.promptUsername = true
        },
        login() {
            if (!this.username) {
                this.username = 'Anonymous'
            }
            this.$localStorage.set('username', this.username)
            this.$localStorage.remove('zeusId')
            this.$router.push('dashboard')
        }
    }
}
</script>
