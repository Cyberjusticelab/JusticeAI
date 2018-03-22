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
            <div id="landing-page-git-master-sha">
              <span id="git-master-sha"> {{ gitMasterSHA }} </span>
            </div>
            <!-- el-dialog for username -->
            <el-dialog :visible.sync="promptUsername" center>
                <form v-on:submit.prevent="login()">
                    <el-input v-model="username" autofocus placeholder="Please Enter Your Name" ref="enteringUsername"></el-input>
                    <el-button native-type="submit" type="primary" v-if="username">Next</el-button>
                    <el-button native-type="submit" type="primary" v-if="!username">Skip</el-button>
                </form>
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
            username: null,
            gitMasterSHA: process.env.GIT_LATEST_MASTER_COMMIT
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
