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
                    <li v-for="file in uploadedFileList">
                        <b-row>
                            <b-col md="6" offset-md="2">
                                <p>{{ file.name }}</p>
                            </b-col>
                            <b-col md="1">
                                <img class="sidebar-file-view" alt="" src="../assets/file_view.png" v-on:click="openUploadedFile(file.id)">
                            </b-col>
                        </b-row>
                    </li>
                </ul>
            </transition>
            <!-- End of Uploaded File List -->
            <!-- Report List -->
            <div id="sidebar-reports" class="sidebar-menu" v-on:click="openReportList = !openReportList; openFileList = false" v-bind:class="{ 'active-menu': openReportList}">
                <h3>REPORTS</h3>
            </div>
            <transition name="fade">
                <ul v-if="openReportList">
                    <li>
                        <b-row>
                            <b-col md="6" offset-md="2">
                                <p>demo.pdf</p>
                            </b-col>
                            <b-col md="1">
                                <img class="sidebar-file-view" alt="" src="../assets/file_view.png">
                            </b-col>
                        </b-row>
                    </li>
                </ul>
            </transition>
            <!-- End Report List -->
            <!-- Previous Case List -->
            <div id="sidebar-previous-case" class="sidebar-menu">
                <h3>PREVIOUS CASES</h3>
            </div>
            <!-- End of Previous Case List -->
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
            username: this.$localStorage.get('usertype').toUpperCase(),
            api_url: process.env.API_URL,
            connectionError: false
        }
    },
    methods: {
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
        },
        openUploadedFile (fileId) {
            let zeusId = this.$localStorage.get('zeusId')
            window.open(this.api_url + 'conversation/'
            + zeusId + '/files/' + fileId)
        }
    }
}
</script>
