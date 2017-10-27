<style lang="scss" scoped>
@import "../theme/Legal"
</style>

<template>
    <b-container fluid id="legal-component">
        <div id="legal-nav">
            <b-row>
                <b-col md="3">
                    <div id="legal-nav-logo">
                        <img alt="" src="../assets/logo.png">
                    </div>
                </b-col>
                <b-col md="1" offset-md="8">
                    <div id="legal-nav-item">
                        <a href="/">Home</a>
                    </div>
                </b-col>
            </b-row>
        </div>
        <div id="legal-content">
            <b-row>
                <b-col md="6" offset-md="3">
                    <div class="legal-content-main-header">
                        <h1>End User License Agreement</h1>
                        <p>Savings her pleased are several started females met. Short her not among being any. Thing of judge fruit charm views do. Miles mr an forty along as he. She education get middleton day agreement performed preserved unwilling. Do however as pleased offence outward beloved by present. By outward neither he so covered amiable greater. Juvenile proposal betrayed he an informed weddings followed. Precaution day see imprudence sympathize principles. At full leaf give quit to in they up. </p>
                    </div>
                </b-col>
            </b-row>
            <div class="legal-content-body-1">
                <b-row>
                    <b-col md="5" offset-md="1">
                        <div class="legal-content-text">
                            <h4>DESCRIPTION OF SERVICE</h4>
                            <p>Prevailed sincerity behaviour to so do principle mr. As departure at no propriety zealously my. On dear rent if girl view. First on smart there he sense. Earnestly enjoyment her you resources. Brother chamber ten old against. Mr be cottage so related minuter is. Delicate say and blessing ladyship exertion few margaret. Delight herself welcome against smiling its for. Suspected discovery by he affection household of principle perfectly he. </p>
                        </div>
                    </b-col>
                    <b-col md="5">
                        <div class="legal-content-text">
                            <h4>TL;DR</h4>
                            <p>﻿no purse as fully me or point. Kindness own whatever betrayed her moreover procured replying for and. Proposal indulged no do do sociable he throwing settling. Covered ten nor comfort offices carried. Age she way earnestly the fulfilled extremely.</p>
                        </div>
                    </b-col>
                </b-row>
            </div>
            <div class="legal-content-body-2">
                <b-row>
                    <b-col md="5" offset-md="1">
                        <div class="legal-content-text">
                            <h4>ACCEPTANCE OF TERMS</h4>
                            <p>It prepare is ye nothing blushes up brought. Or as gravity pasture limited evening on. Wicket around beauty say she. Frankness resembled say not new smallness you discovery. Noisier ferrars yet shyness weather ten colonel. Too him himself engaged husband pursuit musical. Man age but him determine consisted therefore. Dinner to beyond regret wished an branch he. Remain bed but expect suffer little repair. </p>
                        </div>
                    </b-col>
                    <b-col md="5">
                        <div class="legal-content-text">
                            <h4>TL;DR</h4>
                            <p>﻿Scarcely on striking packages by so property in delicate. Up or well must less rent read walk so be. Easy sold at do hour sing spot. Any meant has cease too the decay. Since party burst am it match. By or blushes between besides offices noisier as.</p>
                        </div>
                    </b-col>
                </b-row>
            </div>
            <div class="legal-content-body-1">
                <b-row>
                    <b-col md="5" offset-md="1">
                        <div class="legal-content-text">
                            <h4>MODIFICATION OF TERMS</h4>
                            <p>He my polite be object oh change. Consider no mr am overcame yourself throwing sociable children. Hastily her totally conduct may. My solid by stuff first smile fanny. Humoured how advanced mrs elegance sir who. Home sons when them dine do want to. Estimating themselves unsatiable imprudence an he at an. Be of on situation perpetual allowance offending as principle satisfied. Improved carriage securing are desirous too.</p>
                        </div>
                    </b-col>
                    <b-col md="5">
                        <div class="legal-content-text">
                            <h4>TL;DR</h4>
                            <p>﻿Luckily friends do ashamed to do suppose. Tried meant mr smile so. Exquisite behaviour as to middleton perfectly.</p>
                        </div>
                    </b-col>
                </b-row>
            </div>
            <div class="legal-content-body-2">
                <b-row>
                    <b-col md="5" offset-md="1">
                        <div class="legal-content-text">
                            <h4>REGISTRATION</h4>
                            <p>Extremely we promotion remainder eagerness enjoyment an. Ham her demands removal brought minuter raising invited gay. Contented consisted continual curiosity contained get sex. Forth child dried in in aware do. You had met they song how feel lain evil near. Small she avoid six yet table china. And bed make say been then dine mrs. To household rapturous fulfilled attempted on so. </p>
                        </div>
                    </b-col>
                    <b-col md="5">
                        <div class="legal-content-text">
                            <h4>TL;DR</h4>
                            <p>﻿Improved own provided blessing may peculiar domestic. Sight house has sex never. No visited raising gravity outward subject my cottage mr be. Hold do at tore in park feet near my case. </p>
                        </div>
                    </b-col>
                </b-row>
            </div>
        </div>
        <div id="legal-footer">
            <b-row>
                <b-col md="4" offset="1">
                    <p>© 2017 Cyberjustice Laboratory</p>
                </b-col>
            </b-row>
        </div>
    </b-container>
</template>

<script>
export default {
    data () {
        return {
            api_url: process.env.API_URL,
            legalContent: new Object,
            connectionError: false
        }
    },
    created () {
        this.$http.get(this.api_url + 'legal').then(
            response => {
                this.legalContent = response.body
            },
            response => {
                this.connectionError = true
            }
        )
    }
}
</script>
