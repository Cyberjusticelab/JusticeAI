<style lang="scss" scoped>
@import "../theme/Sidebar"
</style>

<template>
    <div id="sidebar-component">
        <!-- LOGO -->
        <div id="sidebar-logo">
            <img alt="" src="../assets/logo.png">
            <p>Alpha</p>
        </div>
        <!-- End of LOGO -->
        <!-- User Information -->
        <div id="sidebar-account">
            <img alt="" src="../assets/user_avatar_1.png">
            <h2>{{ username }}</h2>
        </div>
        <!-- End of User Information -->
        <!-- Toggle Menu -->
        <div id="sidebar-menu">
            <!-- Uploaded File List -->
            <div id="sidebar-upload-file" class="sidebar-menu" v-on:click="getFileList()" v-bind:class="{ 'active-menu': openFileList}">
                <h3>UPLOADED FILES <span>({{ uploadedFileList.length }})</span></h3>
            </div>
            <transition name="fade">
                <ul v-if="openFileList">
                    <el-row>
                        <li v-for="file in uploadedFileList">
                            <el-col :sm="18">
                                <p>{{ file.name }}</p>
                            </el-col>
                            <el-col :sm="3" :offset="1">
                                <img class="sidebar-file-view" alt="" src="../assets/file_view.png">
                            </el-col>
                        </li>
                    </el-row>
                </ul>
            </transition>
            <!-- End of Uploaded File List -->
            <!-- Report List -->
            <div id="sidebar-reports" class="sidebar-menu" v-on:click="openReportList = !openReportList; openFileList = false" v-bind:class="{ 'active-menu': openReportList}">
                <h3>REPORTS</h3>
            </div>
            <transition name="fade">
                <ul v-if="openReportList">
                    <el-row>
                        <li>
                            <el-col :sm="8" :offset="6">
                                <p>report.pdf</p>
                            </el-col>
                            <el-col :sm="2" :offset="2">
                                <img class="sidebar-file-view" alt="" src="../assets/file_view.png">
                            </el-col>
                        </li>
                    </el-row>
                </ul>
            </transition>
            <!-- End Report List -->
            <!-- Previous Case List -->
            <div id="sidebar-previous-case" class="sidebar-menu">
                <h3>PREVIOUS CASES</h3>
            </div>
            <!-- End of Previous Case List -->
            <!-- Feedback -->
            <div id="sidebar-feedback" class="sidebar-menu" @click="openFeedbackModal = true">
                <h3>FEEDBACK</h3>
            </div>
            <!-- el-dialog for feedback -->
            <el-dialog title="Feedback" :visible.sync="openFeedbackModal">
                <textarea id="feedback-text" v-model="feedback">
                </textarea>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="openFeedbackModal = false">Cancel</el-button>
                    <el-button type="primary" @click="submitFeedback()">Submit</el-button>
                </span>
            </el-dialog>
            <!-- End of el-dialog for feedback -->
            <!-- End of Feedback -->
            <!-- Progress Bar -->
            <div id="sidebar-progress">
            </div>
            <!-- End of Progress Bar -->
        </div>
        <!-- End of Toggle Menu -->
        <!-- Legal -->
        <div id="sidebar-legal">
            <a href="/legal" target="_blank">© 2017 Cyberjustice Laboratory</a>
        </div>
        <!-- End of Legal -->
    </div>
</template>

<script>
export default {
    data () {
        return {
            uploadedFileList: new Array,
            openFileList: false,
            openReportList: false,
            openFeedbackModal: false,
            username: this.$localStorage.get('username').toUpperCase(),
            feedback: '',
            //TODO: fetch username from conversation, now use usertype instead
            api_url: process.env.API_URL,
            connectionError: false
        }
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
        getFileList () {
            if (this.$localStorage.get('zeusId') && !this.openFileList) {
                let zeusId = this.$localStorage.get('zeusId')
                this.$http.get(this.api_url + 'conversation/' + zeusId + '/files').then(
                    response => {
                        if (response.body.files.length > 0) {
                            this.uploadedFileList = response.body.files
                            this.openFileList = true
                            this.openReportList = false
                        } else {
                            this.openFileList = false
                        }
                    },
                    response => {
                        this.connectionError = true
                    }
                )
            } else {
                this.openFileList = false
            }
        }
    }
}
</script>
