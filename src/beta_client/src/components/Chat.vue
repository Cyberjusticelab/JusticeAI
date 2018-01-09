<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!-- UPPER WINDOW: SHOW CHAT -->
    <div id="chat-container" v-chat-scroll>
      <!-- CHAT HISTORY -->
      <div id="chat-history">
        <el-row v-for="history in chatHistory" :key="history.val">
          <el-col :md="{span: 12, offset: 5}" :sm="{span: 20, offset: 2}" :xs="{span: 20, offset: 2}" class="history-message" v-for="set in questionSet[language]" v-if="set.val==history[0]" :key="set.val">
            <p v-html="set.question"></p>
          </el-col>
          <el-col :md="{span: 4, offset: 14}" :sm="{span: 20, offset: 2}" :xs="{span: 20, offset: 2}" class="history-message-user" v-for="set in questionSet[language]" v-if="set.val==history[0]" :key="set.val">
            <p v-if="set.type!=='email' && set.type!=='question'" v-html="set.answer[history[1]]"></p>
            <p v-if="set.type=='question'" v-html="userQuestion"></p>
            <p v-if="set.type=='email'" v-html="userEmail"></p>
          </el-col>
        </el-row>
      </div>
      <!-- END CHAT HISTORY -->
      <!-- CURRENT QUESTION -->
      <div id="chat-current">
        <el-row v-for="set in questionSet[language]" :key="set.val" v-if="set.val == currentQuestion">
          <el-col :md="{span: 4, offset: 1}" :sm="{span: 4, offset: 2}" :xs="{span: 0, offset: 0}">
            <!-- ANIMATED AVATAR -->
            <div id="chat-zeus-avatar">
              <transition name="fade">
                <img v-if="!isZeusThinking" src="../assets/zeus_avatar_1.png"/>
              </transition>
              <transition name="fade">
                <img v-if="isZeusThinking" src="../assets/zeus_avatar_2.png"/>
              </transition>
            </div>
            <!-- END ANIMATED AVATAR -->
          </el-col>
          <el-col :md="{span: 12}" :sm="{span: 16, offset: 0}" :xs="{span: 20, offset: 2}">
            <!-- QUESTION BINDING -->
            <div id="chat-message">
              <div v-if="!isZeusThinking">
                <p v-html="set.question"></p>
                <p id="invalid-answer" v-if="isInvalidInput" v-html="set.error"></p>
              </div>
              <div v-if="isZeusThinking">
                <img src="../assets/chatting.gif"/>
              </div>
            </div>
            <!-- END QUESTION BINDING -->
          </el-col>
        </el-row>
      </div>
      <!-- END CURRENT QUESTION -->
    </div>
    <!-- END UPPER WINDOW: SHOW CHAT -->
    <!-- BOTTOM: SHOW INPUT OPTIONS -->
    <div id="chat-input">
      <el-row v-for="set in questionSet[language]" :key="set.val" v-if="set.val == currentQuestion">
        <el-col v-if="set.type=='question' || set.type=='email'" :md="24">
          <el-input v-if="set.type=='question'" autosize v-model="userQuestion" :placeholder="set.placeholder" autoComplete="off" :disabled="isZeusThinking"></el-input>
          <el-input v-if="set.type=='email'" autosize v-model="userEmail" :placeholder="set.placeholder" :disabled="isZeusThinking"></el-input>
        </el-col>
        <el-col :md="colSize" :sm="colSize" :xs="colSize" v-for="(answer, index) in set.answer" :key="answer.id">
          <el-button type="warning" v-on:click="nextQuestion(set, index)" :disabled="isZeusThinking">{{answer}}</el-button>
        </el-col>
      </el-row>
    </div>
    <!-- END BOTTOM: SHOW INPUT OPTIONS -->
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
      isInvalidInput: false,
      isZeusThinking: false
    }
  },
  props: ['language'],
  methods: {
    nextQuestion (set, skip) {
      this.isZeusThinking = true
      this.validateAnswer(set, skip)
      setTimeout(() => {
        this.isZeusThinking = false
      }, 1100)
    },
    validateAnswer (set, skip) {
      this.isInvalidInput = false
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
      }
      if (!this.isInvalidInput) {
        this.chatHistory.push([this.currentQuestion, skip])
        this.currentQuestion = set.val + 1 + skip;
        if (this.currentQuestion > this.questionSet[this.language].length) {
          this.currentQuestion--
        }
        for (let i = 0; i < this.questionSet[this.language].length; i++) {
          if (this.questionSet[this.language][i].val === this.currentQuestion && this.questionSet[this.language][i].answer) {
            this.colSize = 24/this.questionSet[this.language][i].answer.length
          }
        }
      }
    }
  }
}
</script>
