<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!-- Chat History -->
    <transition name="fade">
      <div id="chat-history" v-if="user.openChatHistory">
        <el-row>
          <el-col :sm="{span: 2, offset: 0}">
            <div id="chat-history-button">
              <img v-on:click="user.openChatHistory = false" alt="" src="../assets/history_disable.png">
            </div>
          </el-col>
          <!-- Chat History ~ Understood Fact -->
          <el-col :sm="{span: 21, offset: 1}">
          <div id="chat-history-fact">
            <el-row v-for="fact in chatHistory.fact" :key="fact.id">
              <el-col :sm="{span: 13, offset: 0}" class="dark-hover">
                <h4>{{ fact.fact.summary }}</h4>
              </el-col>
              <el-col :sm="{span: 4, offset: 0}" class="dark-hover">
                <p>{{ fact.value }}</p>
              </el-col>
              <el-col :sm="{span: 4, offset: 0}">
                <div id="fact-remove">
                  <img alt="" src="../assets/fact_remove.png">
                </div>
                <div id="fact-edit">
                  <img alt="" src="../assets/fact_edit.png">
                </div>
              </el-col>
            </el-row>
          </div>
          </el-col>
          <!-- End Chat History ~ Understood Fact -->
        </el-row>
      </div>
    </transition>
    <!-- End of Chat History -->
    <!-- Chat Widow -->
    <div id="chat-widow">
      <!-- Zeus Chat -->
      <div id="chat-zeus-container">
        <el-row>
          <el-col :sm="{span: 4, offset: 2}">
            <div id="chat-zeus-avatar">
              <img v-on:click="user.openChatHistory = !user.openChatHistory; getChatHistory()" src="../assets/zeus_avatar_1.png"/>
            </div>
          </el-col>
          <el-col :sm="{span: 10, offset: 0}">
            <div id="chat-message-zeus">
              <img v-if="!zeus.input" alt="" src="../assets/chatting.gif">
              <transition name="fade">
                <p v-if="zeus.input" v-html="zeus.input"></p>
              </transition>
              <transition name="fade">
                <file-upload
                  ref="upload"
                  v-model="zeus.file"
                  :drop="true"
                  :post-action="uploadUrl"
                  v-if="zeus.filePrompt"
                  extensions="jpg,jpeg,pdf,docx,webp,png"
                >
                  <p v-if="zeus.file.length == 0" id="drag-and-drop">drag and drop or click to select file</p>
                  <p v-if="zeus.file" id="file-name" v-for="file in zeus.file">{{ file.name }}</p>
                </file-upload>
              </transition>
              <div id="file-upload-button-group" v-if="zeus.filePrompt">
                <el-button v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true" type="warning" :disabled="zeus.file.length == 0">
                  Upload
                </el-button>
                <el-button v-show="$refs.upload && $refs.upload.active" @click.prevent="$refs.upload.active = false" type="warning">
                  Stop
                </el-button>
                <p v-if="zeus.file[0] && zeus.file[0].success && $refs.upload.uploaded">
                  Successfully uploaded <span>{{ zeus.file[0].name }}</span>
                </p>
              </div>
              <div id="pre-selected-answer-group" v-if="zeus.suggestion && zeus.input">
                <el-button v-for="answer in zeus.suggestion" :key="answer.id" type="warning" v-on:click="user.input = answer; sendUserMessage()">
                  {{ answer }}
                </el-button>
              </div>
              <div id="beta-feedback-group" v-if="promptFeedback">
                <div v-on:click="sendFeedback(true)">
                  <icon name="thumbs-up" class="feedback-good"></icon>
                </div>
                <div v-on:click="sendFeedback(false)">
                  <icon name="thumbs-down" class="feedback-bad"></icon>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of Zeus Chat -->
      <!-- User Chat -->
      <div id="chat-user-container">
        <el-row>
          <el-col :sm="14" :offset="8">
            <div id="chat-message-user" v-bind:class="{ msgIsSent: user.isSent && chatHistory.history}">
              <img v-if="!user.input" alt="" src="../assets/chatting.gif">
              <p v-if="user.input" v-html="user.input"></p>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of User Chat -->
    </div>
    <!-- End of Chat Widow -->
    <!-- Input Widow -->
    <div id="chat-input">
      <form v-on:submit.prevent="sendUserMessage()">
        <el-input id="chat-input-text" autosize v-model="user.input" placeholder="Enter your message" autoComplete="off" :disabled="user.disableInput"></el-input>
        <el-button id="chat-input-submit" type="warning" :disabled="!user.input" native-type="submit">SEND</el-button>
      </form>
      <!--<icon id="chat-input-voice" name="microphone" scale="3"></icon>-->
    </div>
    <!-- End of Input Widow -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      api_url: process.env.API_URL,
      uploadUrl: new String,
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
        filePrompt: false,
        suggestion: new Array
      },
      user: {
        name: null,
        input: null,
        isSent: false,
        openChatHistory: false,
        disableInput: false
      }
    }
  },
  created () {
    if (this.$localStorage.get('zeusId')) {
      this.getChatHistory()
    } else {
      this.initChatSession()
    }
  },
  methods: {
    handleEdit (index, row) {
      // TODO: bind event and api
    },
    handleDelete (index, row) {
      // TODO: bind event and api
    },
    initChatSession () {
      this.$http.post(this.api_url + 'new', {
        name: this.$localStorage.get('username'),
        person_type: this.$localStorage.get('usertype')
      }).then(
        response => {
          this.$localStorage.set('zeusId', response.body.conversation_id)
          this.user.input = ''
          this.sendUserMessage()
          this.uploadUrl = this.api_url + 'conversation/' + response.body.conversation_id + '/files'
        },
        response => {
          this.connectionError = true
        }
      )
    },
    sendUserMessage () {
      this.$http.post(this.api_url + 'conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.user.input
      }).then(
        response => {
          this.zeus.input = null
          this.user.isSent = this.user.input != ''
          this.zeus.filePrompt = false;
          this.numMessageSinceChatHistory += 1
          setTimeout(() => {
            this.configChat(response.body)
          }, 1100)
        },
        response => {
          this.connectionError = true
        }
      )
    },
    getChatHistory () {
      let zeusId = this.$localStorage.get('zeusId')
      this.$http.get(this.api_url + 'conversation/' + zeusId).then(
        response => {
          this.chatHistory.history = response.body.messages
          this.chatHistory.fact = response.body.fact_entities
          this.numMessageSinceChatHistory = 0
          this.user.name = response.body.name
          if (!this.zeus.input) {
            this.configChat(this.chatHistory.history[this.chatHistory.history.length - 1])
          }
          this.uploadUrl = this.api_url + 'conversation/' + zeusId + '/files'
          this.promptFeedback = this.numMessageSinceChatHistory + this.chatHistory.history.length > 4
        },
        response => {
          this.connectionError = true
        }
      )
    },
    configChat (conversation) {
      this.zeus.input = conversation.message || conversation.html || conversation.text
      this.zeus.filePrompt = (conversation.file_request !== undefined) && (conversation.file_request !== null)
      if (conversation.possible_answers == undefined) {
        this.zeus.suggestion = []
      } else {
        this.zeus.suggestion = JSON.parse(conversation.possible_answers) || []
      }
      this.numMessageSinceChatHistory += 1
      this.promptFeedback = this.numMessageSinceChatHistory + this.chatHistory.history.length > 4
      this.user.input = null
      this.user.isSent = false
      this.user.disableInput = conversation.enforce_possible_answer
      this.promptFeedback = true
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
          this.promptFeedback = false
          this.connectionError = true
        }
      )
    }
  }
}
</script>
