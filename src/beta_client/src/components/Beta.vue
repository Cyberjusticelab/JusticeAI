<style lang="scss" scoped>
@import "../theme/Beta"
</style>

<template>
    <el-container id="beta-component">
        <div id="beta-page">
            <div id="beta-page-nav">
                <p v-on:click="aboutUs=!aboutUs" v-if="!aboutUs">ABOUT US</p>
            </div>
            <div id="beta-page-lang">
                <p v-on:click="changeLanguage('fr')" v-if="language != 'fr'">FRANCAIS</p>
                <p v-on:click="changeLanguage('en')" v-if="language != 'en'">ENGLISH</p>
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
                    <chat :language="language"></chat>
                </div>
            </transition>
            <transition name="fade">
                <div id="beta-page-button-group">
                    <el-row>
                        <el-col :md="24">
                            <div id="button-group">
                                <el-button type="warning" v-if="!chat" v-on:click="chat = !chat">SIGN UP TO BETA</el-button>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </transition>
        </div>
        <transition name="fade">
            <div id="beta-page-about-us" v-if="aboutUs">
                <div id="beta-page-about-us-nav">
                    <p v-on:click="aboutUs=!aboutUs">CLOSE</p>
                </div>
                <h2>Cyberjustice Laboratory</h2>
                <img alt="" src="../assets/cjl.jpg" id="beta-page-zeus">
                <div class="about-us-text">
                    <p>The Cyberjustice Lab is a hub for thought and creativity, where justice processes are modelled and reimagined. More specifically, the Laboratory analyses the impact of technologies on justice and develops concrete technological tools that are adapted to the reality of justice systems.</p>
                    <p>Hosted at the Faculty of Law of the Université de Montréal, its multidisciplinary international research team extends to 45 researchers from 23 institutions in Europe, the Americas, China and Australia, whose investigative goals tend towards improving the allocation and administration of judicial services so as to make optimal use of advances in technology.</p>
                    <p>The Cyberjustice Laboratory is designing an artificial intelligence tool capable of assessing the validity of a litigant’s claim and proposing possible avenues for resolution.</p>
                    <p>The solution takes the shape of a dynamic conversational agent designed to predict the likely outcomes of a variety of landlord/tenant disputes, based on personalized interactions with the disputant and analysis of relevant case law using machine learning algorithms.</p>
                    <p>The project tests the boundaries of machine learning and natural language processing applied to the complex domain of law, and attempts to validate the utility of such a tool for stakeholders.</p>
                </div>
            </div>
        </transition>
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
            chat: false,
            aboutUs: false,
            language: 'en'
        }
    },
    created () {
        if (this.langQuery == 'fr'){
            this.language = this.langQuery
        }
    },
    methods: {
        changeLanguage (lang) {
            this.language = lang
            this.$router.replace({path: '/', query: {lang: lang}})
        }
    },
    props: ['langQuery'],
}
</script>
