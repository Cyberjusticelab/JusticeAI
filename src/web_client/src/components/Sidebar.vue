<style lang="scss" scoped>
@import "../theme/Sidebar"
</style>

<template>
    <div id="sidebar-component" v-bind:class="{ 'burger-menu': !openSidebar }">
        <!-- 1. Menu Close -->
        <div v-if="!openSidebar" v-on:click="openSidebar = true" id="sidebar-min">
            <img alt="" src="../assets/sidebar-toggle.png">
        </div>
        <!-- 1. End of Menu Close -->
        <!-- 2.1 Menu Open -->
        <transition name="translate">
            <div v-if="openSidebar" id="sidebar-full">
                <!-- LOGO -->
                <div id="sidebar-logo">
                    <img alt="" src="../assets/logo.png" v-on:click="openSidebar = false">
                    <p>Beta</p>
                </div>
                <!-- End of LOGO -->
                <!-- Pending Info -->
                <div id="sidebar-dashboard">
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
            username: this.$localStorage.get('username'),
            usertype: this.$localStorage.get('usertype'),
            feedback: '',
            //TODO: fetch username from conversation, now use usertype instead
            api_url: process.env.API_URL,
            connectionError: false
        }
    },
    created () {
        EventBus.$on('hideSidebar', () => {
            this.openSidebar = false
        })
    },
    methods: {
        submitFeedback(){
            if (this.feedback) {
                this.$http.post(this.api_url + 'feedback',{
                    feedback: this.feedback
                }).then(
                    response => {
                        alert("Thank you for providing us with feedback!");
                        this.openFeedbackModal = false;
                        this.feedback = '';
                    },
                    response => {
                        this.connectionError = true
                        alert("Sorry, an error occurred and we could not receive your feedback.");
                        this.openFeedbackModal = false;
                        this.feedback = '';
                    }
                )
            } else {
                alert("No feedback entered");
            }
        },
        resetChat () {
            this.$localStorage.remove('zeusId')
            this.$localStorage.remove('username')
            this.$localStorage.remove('usertype')
            this.$router.push('/')
        }
    }
}
</script>
