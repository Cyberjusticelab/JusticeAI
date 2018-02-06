<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!-- UPPER WINDOW: SHOW CHAT -->
    <div id="chat-container">
      <!-- CHAT HISTORY -->
      <div id="chat-history">
        <el-row v-for="history in chatHistory" :key="history.val">
          <span v-for="set in questionSet[language]" v-if="set.val==history[0]" :key="set.val">
            <el-col :md="{span: 12, offset: 5}" :sm="{span: 18, offset: 2}" :xs="{span: 18, offset: 2}" v-for="(question, index) in set.question" :key="index" class="history-message">
              <p v-html="question"></p>
            </el-col>
          </span>
          <el-col :md="{span: 4, offset: 14}" :sm="{span: 18, offset: 4}" :xs="{span: 18, offset: 4}" class="history-message-user" v-for="set in questionSet[language]" v-if="set.val==history[0]" :key="set.val">
            <p v-if="set.type!=='email' && set.type!=='question'" v-html="set.answer[history[1]]"></p>
            <p v-if="set.type=='question'" v-html="userQuestion"></p>
            <p v-if="set.type=='email'" v-html="userEmail"></p>
          </el-col>
        </el-row>
        <el-row v-for="set in questionSet[language]" :key="set.val" v-if="set.val == currentQuestionIndex">
            <el-col :md="{span: 12, offset: 5}" :sm="{span: 18, offset: 2}" :xs="{span: 18, offset: 2}" v-for="(question, index) in set.question" :key="index" v-if="currentStatementIndex > set.question.indexOf(question)" class="history-message">
              <p v-html="question"></p>
            </el-col>
        </el-row>
      </div>
      <!-- END CHAT HISTORY -->
      <!-- CURRENT QUESTION -->
      <el-col :md="{span: 20, offset: 2}" id="chat-current">
        <el-row v-for="set in questionSet[language]" :key="set.val" v-if="set.val == currentQuestionIndex">
          <el-col :md="{span: 4, offset: 1}" :sm="{span: 4, offset: 2}" :xs="{span: 0, offset: 0}">
            <!-- ANIMATED AVATAR -->
            <div id="chat-zeus-avatar">
                <img v-if="!isZeusThinking" src="../assets/zeus_avatar_1.png"/>
                <img v-if="isZeusThinking" src="../assets/zeus_avatar_2.png"/>
            </div>
            <!-- END ANIMATED AVATAR -->
          </el-col>
          <el-col :md="{span: 12}" :sm="{span: 16, offset: 0}" :xs="{span: 20, offset: 2}">
            <!-- QUESTION BINDING -->
            <el-col class="chat-message" v-if="!isZeusThinking">
              <div>
                <p v-html="set.question[currentStatementIndex]"></p>
                <p id="invalid-answer" v-if="isInvalidInput" v-html="set.error"></p>
                <form v-on:submit.prevent="nextQuestion(set, 0)" v-if="set.question.length - 1 == currentStatementIndex && set.val == currentQuestionIndex" v-for="set in questionSet[language]" :key="set.val">
                  <el-row>
                    <el-col v-if="set.type=='question' || set.type=='email'" :md="24">
                      <el-input v-if="set.type=='question'" autosize v-model="userQuestion" :placeholder="set.placeholder" autoComplete="off" :disabled="isZeusThinking"></el-input>
                      <el-input v-if="set.type=='email'" autosize v-model="userEmail" :placeholder="set.placeholder" :disabled="isZeusThinking"></el-input>
                    </el-col>
                    <el-col class="answer-button" :md="colSize" :sm="colSize" :xs="colSize" v-for="(answer, index) in set.answer" :key="answer.id">
                      <el-button type="warning" v-on:click="nextQuestion(set, index)" :disabled="isZeusThinking">{{answer}}</el-button>
                    </el-col>
                  </el-row>
                </form>
              </div>
            </el-col>
            <!-- END QUESTION BINDING -->
            <div class="chat-message" v-if="isZeusThinking">
                <img src="../assets/chatting.gif"/>
            </div>
          </el-col>
          <el-col id="chat-marker"></el-col>
        </el-row>
      </el-col>
      <!-- END CURRENT QUESTION -->
    </div>
    <!-- END UPPER WINDOW: SHOW CHAT -->
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
      currentQuestionIndex: 1,
      currentStatementIndex: 0,
      chatHistory: new Array,
      colSize: 24,
      userEmail: null,
      userQuestion: null,
      userId: null,
      isInvalidInput: false,
      isZeusThinking: false
    }
  },
  props: ['language'],
  created () {
    this.nextStatement(locale[this.language][0])
  },
  methods: {
    nextQuestion (set, skip) {
      this.isZeusThinking = true
      this.validateAnswer(set, skip)
      if (!this.isInvalidInput) {
        set = this.updateQuestion(set, skip)
      }
      var self = this
      self.$nextTick(() => self.$el.querySelector('#chat-marker').scrollIntoView())
      setTimeout(() => {
        self.isZeusThinking = false
        self.$nextTick(() => self.$el.querySelector('#chat-marker').scrollIntoView())
        if (!self.isInvalidInput){
          self.nextStatement(set)
        }
      }, 1500 - Math.random() * 500)
    },
    nextStatement (set) {
      if (this.currentStatementIndex < set.question.length - 1) {
        var self = this
        setTimeout(() => {
          self.isZeusThinking = true
          self.currentStatementIndex++
          self.$nextTick(() => self.$el.querySelector('#chat-marker').scrollIntoView())
          setTimeout(() => {
            self.isZeusThinking = false
            self.$nextTick(() => self.$el.querySelector('#chat-marker').scrollIntoView())
            self.nextStatement(set)
          }, 1500 - Math.random() * 500)
        }, 2000 + Math.random() * 1000)
      }
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
      } else if (set.type === 'isPro' && skip === 0) {
        this.$http.put(this.api_url + 'legal', {
          id: this.userId,
          is_legal_professional: skip
        })
      }
    },
    updateQuestion (set, skip) {
      this.chatHistory.push([this.currentQuestionIndex, skip])
      this.currentStatementIndex = 0
      this.currentQuestionIndex = set.val + 1 + skip;
      if (this.currentQuestionIndex > this.questionSet[this.language].length) {
        this.currentQuestionIndex--
      }
      for (let i = 0; i < this.questionSet[this.language].length; i++) {
        if (this.questionSet[this.language][i].val === this.currentQuestionIndex) {
          if (this.questionSet[this.language][i].answer) {
            this.colSize = 24/this.questionSet[this.language][i].answer.length
          }
          return this.questionSet[this.language][i]
        }
      }
    }
  }
}
</script>
