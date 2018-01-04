<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!--
    <div id="chat-container">
      <el-row v-for="set in questionSet[language]" :key="set.val">
        <el-col :sm="{span: 4, offset: 1}" :xs="{span: 24}">
          <div id="chat-zeus-avatar" v-if="heyhey">
            <img src="../assets/zeus_avatar_1.png"/>
          </div>
        </el-col>
        <el-col :sm="{span: 18}" :xs="{span: 22, offset: 1}">
          <div id="chat-message-zeus">
            <div>
              <p v-html="set.question"></p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>-->
    <div id="chat-input">
      <el-row v-for="set in questionSet[language]" :key="set.val" v-if="set.val == currentQuestion">
        <el-col v-if="set.type=='question' || set.type=='email'" :md="24">
          <el-input v-if="set.type=='question'" autosize v-model="userQuestion" :placeholder="set.placeholder" autoComplete="off"></el-input>
          <el-input v-if="set.type=='email'" autosize v-model="userEmail" :placeholder="set.placeholder"></el-input>
        </el-col>
        <el-col :md="colSize" v-for="(answer, index) in set.answer" :key="answer.id">
          <el-button type="warning" v-on:click="validateAnswer(set, index)">{{answer}}</el-button>
        </el-col>
      </el-row>
      <el-row>
        <transition name="fade">
          <p id="invalid-answer" v-if="isInvalidInput">Please make sure your input is valid and not empty, thanks!</p>
        </transition>
      </el-row>
    </div>
  </div>
</template>

<script>
import locale from '../assets/locale.json'
export default {
  name: 'Chat',
  data () {
    return {
      api_url: process.env.API_URL,
      questionSet: locale,
      currentQuestion: 1,
      chatHistory: new Array,
      colSize: 24,
      userEmail: null,
      userQuestion: null,
      userSubscription: false,
      userId: null,
      isInvalidInput: false
    }
  },
  props: ['language'],
  methods: {
    validateAnswer (set, skip) {
      this.isInvalidInput = false
      console.log(skip)
      if (set.type === 'question') {
        if (this.userQuestion) {
          this.$http.post(this.api_url + 'question', {
            question: this.userQuestion
          }).then(
            response => {
              this.userId = response.data.id
            }
          )
        } else {
          this.isInvalidInput = true
        }
      } else if (set.type === 'email') {
        if (/^.+@[a-zA-Z0-9\-]+\.[a-zA-Z]+$/.test(this.userEmail)) {
          this.$http.put(this.api_url + 'email', {
            id: this.userId,
            email: this.userEmail
          })
        } else {
          this.isInvalidInput = true
        }
      } else if (set.type === 'subscription') {
        this.$http.put(this.api_url + 'subscription', {
          id: this.userId,
          is_subscribed: 1
        })
      } else if (set.val == -1) {
        this.$router.go('/')
      }
      if (!this.isInvalidInput) {
        this.currentQuestion = set.val + 1 + skip;
        for (let i = 0; i < this.questionSet[this.language].length; i++) {
          if (this.questionSet[this.language][i].val === this.currentQuestion) {
            this.colSize = 24/this.questionSet[this.language][i].answer.length
          }
        }
      }
    }
  }
}
</script>
