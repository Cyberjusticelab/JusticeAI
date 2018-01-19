<style lang="scss" scoped>
@import "../theme/Beta";
</style>

<template>
    <el-container id="beta-component">
        <div id="beta-page">
            <div id="beta-page-top">
                <el-row>
                    <el-col :md="{span: 12, offset: 1}">
                        <div id="title-image">
                            <img alt="" src="../assets/beta_page_zeus_avatar.png" id="beta-page-zeus">
                            <img alt="" src="../assets/beta_page_logo.png" id="beta-page-logo">
                        </div>
                    </el-col>
                    <el-col :md="{span: 4, offset: 7}">
                        <div id="beta-page-nav">
                            <p v-on:click="changeLanguage('fr')" v-if="language != 'fr'">FRANCAIS</p>
                            <p v-on:click="changeLanguage('en')" v-if="language != 'en'">ENGLISH</p>
                            <p v-on:click="aboutUs=!aboutUs" v-if="!aboutUs">ABOUT US</p>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div id="beta-page-sign-up">
                <chat :language="language"></chat>
            </div>
        </div>
        <transition name="translate">
            <div id="beta-page-about-us" v-if="aboutUs">
                <div id="beta-page-about-us-nav">
                    <p v-on:click="aboutUs=!aboutUs">CLOSE</p>
                </div>
                <h2>About the Cyberjustice Laboratory</h2>
                <img alt="" src="../assets/cjl.jpg" id="beta-page-zeus">
                <div class="about-us-text">
                    <p>The Cyberjustice Lab is a hub for thought and creativity, where justice processes are modelled and reimagined. More specifically, the Laboratory analyses the impact of technologies on justice and develops concrete technological tools that are adapted to the reality of justice systems.</p>
                    <p>Hosted at the Faculty of Law of the Université de Montréal, its multidisciplinary international research team extends to 45 researchers from 23 institutions in Europe, the Americas, China and Australia, whose investigative goals tend towards improving the allocation and administration of judicial services so as to make optimal use of advances in technology.</p>
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
