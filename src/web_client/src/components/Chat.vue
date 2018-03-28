<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!-- Resolved Fact Overlay -->
    <transition name="fade">
      <div id="chat-resolved-fact" v-if="user.openChatHistory">
        <el-row>
          <el-col :sm="{span: 2, offset: 0}">
            <div id="chat-resolved-fact-button">
              <img v-on:click="user.openChatHistory = false" alt="" src="../assets/history_disable.png">
            </div>
          </el-col>
          <el-col :sm="{span: 21, offset: 1}">
          <div id="chat-resolved-fact-item">
            <el-row v-for="fact in chatHistory.fact" :key="fact.id">
              <el-col :sm="{span: 13, offset: 0}" class="dark-hover">
                <h4>{{ fact.fact.summary }}</h4>
              </el-col>
              <el-col :sm="{span: 4, offset: 0}" class="dark-hover">
                <p>{{ fact.value }}</p>
              </el-col>
              <el-col :sm="{span: 4, offset: 0}">
                <div id="fact-remove">
                  <img alt="" src="../assets/fact_remove.png" v-on:click="removeFact(fact.id)">
                </div>
              </el-col>
            </el-row>
          </div>
          </el-col>
          <!-- End Chat History ~ Understood Fact -->
        </el-row>
      </div>
    </transition>
    <!-- End of Resolved Fact Overlay -->
    <!-- Chat Window -->
    <div id="chat-window" ref="mainWindow">
      <!-- Zeus Chat -->
      <div id="chat-history-container">
        <div v-for="(history, index1) in chatHistory.history" :key="index1">
          <el-row v-for="(sentence, index2) in history.text" :key="index2" v-if="!(index1 == chatHistory.history.length-1 && index2 == history.text.length-1)">
            <el-col :sm="{span: 14, offset: 2}">
              <div class="chat-history-zeus" v-if="history.sender_type == 'BOT'">
                <p v-html="sentence"></p>
              </div>
            </el-col>
            <el-col :sm="{span: 12, offset: 8}" v-if="history.sender_type == 'USER'">
              <div class="chat-history-user">
                <p v-html="sentence"></p>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
      <div id="chat-current-container">
        <el-row>
          <el-col :sm="{span: 3, offset: 2}">
            <div id="chat-zeus-avatar" v-on:click="user.openChatHistory = !user.openChatHistory; getFact()"></div>
          </el-col>
          <el-col :sm="{span: 12, offset: 0}">
            <div id="chat-zeus-message">
              <img v-if="zeus.isThinking" alt="" src="../assets/chatting.gif">
              <transition name="fade">
                <p class="zeus-chat-text" v-if="!zeus.isThinking" v-html="zeus.input"></p>
              </transition>
              <div id="pre-selected-answer-group" v-if="zeus.suggestion && !zeus.isSpeaking && !zeus.isThinking">
                <el-button v-for="answer in zeus.suggestion" :key="answer.id" type="warning" v-on:click="user.input = answer; sendUserMessage()">
                  {{ answer }}
                </el-button>
              </div>
              <div id="beta-feedback-group" v-if="promptFeedback && !zeus.isSpeaking && !zeus.isThinking">
                <div v-on:click="sendFeedback(true)">
                  <icon name="thumbs-up" class="feedback-good"></icon>
                </div>
                <div v-on:click="sendFeedback(false)">
                  <icon name="thumbs-down" class="feedback-bad"></icon>
                </div>
              </div>
              <div id="bubble-input-group" v-if="zeus.input">
                <form v-on:submit.prevent="sendUserMessage()" v-if="zeus.suggestion.length == 0 && !zeus.isSpeaking && !zeus.isThinking">
                  <el-input autosize v-model="user.input" placeholder="Enter your message" autoComplete="off" :disabled="user.disableInput" autofocus></el-input>
                  <el-button type="warning" :disabled="!user.input" native-type="submit">SEND</el-button>
                </form>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of Zeus Chat -->
    </div>
    <!-- End of Chat Window -->
  </div>
</template>

<script>
import { EventBus } from './EventBus.js'
import tippy from 'tippy.js'
import Constants from '@/constants'
export default {
  data () {
    return {
      api_url: process.env.API_URL,
      connectionError: false,
      numMessageSinceChatHistory: 0,
      promptFeedback: false,
      isLoggedIn: false, //TODO: account feature
      chatHistory: {
        history: new Array,
        fact: new Array
      },
      zeus: {
        input: null,
        file: new Array,
        suggestion: new Array,
        isThinking: false,
        isSpeaking: false,
        progress: 0
      },
      user: {
        name: null,
        input: null,
        openChatHistory: false,
        disableInput: false
      }
    }
  },
  created () {
    let zeusId = this.$localStorage.get('zeusId')
    /*
    1. resume conversation if user exists
    */
    if (zeusId) {
      this.$http.get(this.api_url + 'conversation/' + zeusId).then(
        response => {
          // 1.1 save chat history in local and parse the sentences
          this.chatHistory.history = response.body.messages
          for (let i = 0; i < this.chatHistory.history.length; i++) {
            this.chatHistory.history[i].text = this.chatHistory.history[i].text.split('|')
              .map((sentence) => { return this.addHover(sentence) })
          }
          // 1.2 save resolved fact in local
          this.chatHistory.fact = response.body.fact_entities
          // 1.3 save user name
          this.user.name = response.body.name
          // 1.4 set counter for feedback prompt
          this.numMessageSinceChatHistory = this.chatHistory.history.length
          this.promptFeedback = this.numMessageSinceChatHistory > 4
          // 1.5 resume conversation from last message
          this.configChat(this.chatHistory.history[this.chatHistory.history.length - 1])
          // 1.6 disable loading bar
          EventBus.$emit('initLoading', false)
        },
        response => {
          this.connectionError = true
          console.log("Connection Fail: init - get history")
        }
      )
    /*
    2. init new conversation if new user
    */
    } else {
      this.$http.post(this.api_url + 'new', {
        name: this.$localStorage.get('username'),
        person_type: this.$localStorage.get('usertype')
      }).then(
        response => {
          // 2.1 store conversation id
          this.$localStorage.set('zeusId', response.body.conversation_id)
          // 2.2 init new conversation session by sending empty string
          this.user.input = ''
          this.sendUserMessage()
          EventBus.$emit('initLoading', false)
        },
        response => {
          this.connectionError = true
          console.log("Connection Fail: init - new user")
        }
      )
    }
  },
  methods: {
    addHover (text) {
      return text
        .split(' ')
        .map((word) => {
          if (Constants.difficult_word_definitions[word.toLowerCase()] !== undefined){
            return '<span class="hoverable" title="' + Constants.difficult_word_definitions[word.toLowerCase()] +'" style="background-color: #f5af5380;border-radius: 3px;padding: 2px; cursor:pointer;">' + word + '</span>'
          }
          return word
        })
        .join(' ')
    },
    sendUserMessage () {
      this.user.disableInput = true
      this.$http.post(this.api_url + 'conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.user.input
      }).then(
        response => {
          this.configChat(response.body)
        },
        response => {
          this.user.disableInput = false
          this.connectionError = true
          console.log("Connection Fail: send message")
        }
      )
    },
    configChat (conversation) {
      this.zeus.isThinking = true
      setTimeout(() => {
        this.zeus.isThinking = false
      }, 1500)
      // 1. push user input to history
      if (this.user.input) {
        this.chatHistory.history.push({
          text: [this.user.input],
          sender_type: 'USER'
        })
      }
      // 2. set current zeus response
      let zeusResponseText = conversation.message || conversation.text
      if (typeof zeusResponseText === 'string') {
        zeusResponseText = this.addHover(zeusResponseText)
      } else {
        zeusResponseText = zeusResponseText.map((sentence) => { return this.addHover(sentence) })
      }
      // 2.1 if from history, show the last sentence
      if (!this.zeus.input && this.chatHistory.history.length > 0) {
        this.zeus.input = zeusResponseText.slice(-1)[0]
      // 2.2 if from new response, repeatly show the sentences and push to history
      } else {
        this.zeus.isSpeaking = true
        zeusResponseText = zeusResponseText.split('|')
        conversation.text = new Array
        conversation.sender_type = 'BOT'
        this.chatHistory.history.push(conversation)
        for (let i = 0; i < zeusResponseText.length; i++) {
          setTimeout(() => {
            this.zeus.input = zeusResponseText[i]
            this.chatHistory.history[this.chatHistory.history.length-1].text.push(zeusResponseText[i])
            if (i == zeusResponseText.length - 1) {
              this.zeus.isSpeaking = false
            }
            this.$refs.mainWindow.scrollTop = this.$refs.mainWindow.scrollHeight
          }, 2500*i)
        }
      }
      // 3. set if pre-selected answer buttons
      if (conversation.possible_answers == undefined) {
        this.zeus.suggestion = []
      } else {
        this.zeus.suggestion = JSON.parse(conversation.possible_answers) || []
      }
      // 4. set progress
      this.zeus.progress = conversation.progress || 0
      this.updateSidebarEvent(this.zeus.progress)
      // 5. set feedback prompt
      this.numMessageSinceChatHistory += 1
      this.promptFeedback = this.numMessageSinceChatHistory > 4
      // 6. reset user input to empty
      this.user.input = null
      this.user.disableInput = conversation.enforce_possible_answer
      tippy('.hoverable')
    },
    sendFeedback (confirmation) {
      this.$http.post(this.api_url + 'store-user-confirmation', {
        conversation_id: this.$localStorage.get('zeusId'),
        confirmation: confirmation || false
      }).then(
        response => {
          this.promptFeedback = false
        },
        response => {
          this.connectionError = true
          console.log("Connection Fail: send feedback")
        }
      )
    },
    getFact () {
      let zeusId = this.$localStorage.get('zeusId')
      this.$http.get(this.api_url + 'conversation/' + zeusId + '/resolved').then(
        response => {
          this.chatHistory.fact = response.body.fact_entities
        },
        response => {
          this.connectionError = true
          console.log("Connection Fail: get resolved fact")
        }
      )
    },
    removeFact (factId) {
      let zeusId = this.$localStorage.get('zeusId')
      this.$http.delete(this.api_url + 'conversation/' + zeusId + '/resolved/' + factId).then(
        response => {
          this.getFact()
        },
        response => {
          this.connectionError = true
          console.log("Connection Fail: remove resolved fact")
        }
      )
    },
    updateSidebarEvent (progress) {
      if (progress && progress > 0) {
        this.$localStorage.set('progress', progress)
        EventBus.$emit('updateSidebar')
      }
    }
  }
}
</script>
