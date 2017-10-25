<style lang="scss" scoped>
@import "../theme/Sidebar"
</style>

<template>
    <div id="sidebar-component">
        <div id="sidebar-logo">
            <img alt="" src="../assets/logo.png">
            <p>Alpha</p>
        </div>
        <div id="sidebar-account">
            <img alt="" src="../assets/user_avatar_1.png">
            <h2>BRUCE CAI</h2>
        </div>
        <div id="sidebar-menu">
            <div id="sidebar-upload-file" class="sidebar-menu" v-on:click="openFileList = !openFileList" v-bind:class="{ 'active-menu': openFileList}">
                <h3>UPLOADED FILES</h3>
            </div>
            <transition name="fade">
                <ul v-if="openFileList">
                    <li v-for="(file, key) in uploadedFileList">
                        <p>{{ file.name }}</p>
                        <img alt="" src="../assets/file_download.png">
                        <img alt="" src="../assets/file_view.png">
                    </li>
                </ul>
            </transition>
            <div id="sidebar-reports" class="sidebar-menu">
                <h3>REPORTS</h3>
            </div>
            <div id="sidebar-previous-case" class="sidebar-menu">
                <h3>PREVIOUS CASES</h3>
            </div>
            <div id="sidebar-progress">

            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            uploadedFileList: {
                file1: {
                    name: 'Lease.pdf'
                },
                file2: {
                    name: 'Agreement.pdf'
                }
            },
            openFileList: false
        }
    }
}
</script>
