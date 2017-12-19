<style lang="scss" scoped>
@import "../theme/beta"
</style>

<template>
    <el-container id="beta-component">
        <div id="beta-page">
            <div id="beta-page-nav">
                <p>ABOUT US</p>
            </div>
            <transition name="fade">
                <div id="beta-page-title" v-bind:class="{ 'beta-page-title-in-chat': chat}">
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
            </transition>
            <transition name="fade">
                <div id="beta-page-sign-up" v-if="chat">
                    <div id="beta-page-sign-up-nav">
                        <img alt="" src="../assets/close.png" v-on:click="$router.go('/')">
                        <p v-on:click="$router.go('/')">Back</p>
                    </div>
                    <chat></chat>
                </div>
            </transition>
            <transition name="fade">
                <div id="beta-page-button-group" v-if="!chat">
                    <el-row>
                        <el-col :md="24">
                            <div id="button-group">
                                <el-button type="warning" v-on:click="chat = !chat">SIGN UP TO BETA</el-button>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </transition>
            <div id="beta-page-footer">
                <a href="http://www.cyberjustice.ca/" target="_blank">© 2017 Cyberjustice Laboratory</a>
            </div>
        </div>
        <!-- about us section todo
        <div id="beta-page-about-us">
            <p>dsad</p>
        </div>
        -->
    </el-container>
</template>

<script>
import Chat from './Chat'

export default {
    components: {
        Chat
    },
    data () {
        return {
            chat: false
        }
    }
}
</script>
