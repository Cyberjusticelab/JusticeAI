<style lang="scss" scoped>
 @import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
    <!-- Chat Widow -->
    <div id="chat-widow">
      <!-- Zeus Chat -->
      <div id="chat-zeus-container">
        <el-row>
          <el-col :sm="4">
            <div id="chat-zeus-avatar">
              <img src="../assets/zeus_avatar_2.png"/>
            </div>
          </el-col>
          <el-col :sm="19">
            <div id="chat-message-zeus">
              <img v-if="!zeus.input" alt="" src="../assets/chatting.gif">
              <transition name="fade">
                <div>
                  <p v-if="zeus.input" v-html="zeus.input"></p>
                </div>
              </transition>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of Zeus Chat -->
    </div>
    <!-- End of Chat Widow -->
    <!-- Input Widow -->
    <div id="chat-input">
      <el-row>
        <el-col :span="user.inputSize" v-for="item in user.inputs" :key="item.text">
          <el-button id="chat-input-submit" type="warning" v-on:click="nextChat(item.val)">{{item.text}}</el-button>
        </el-col>
      </el-row>
    </div>
    <!-- End of Input Widow -->
  </div>
</template>

<script>
export default {
  // State Values
  // 0 : Regular flow
  // 1 : Does not want to provide question
  // 2 : Does not want to provide email
  // 3 : Show Question Input // TODO
  // 4 : Show Email Input // TODO
  name: 'Chat',
  data () {
    return {
      api_url: process.env.API_URL,
      counter: 0,
      currentMap: [],
      connectionError: false,
      regularConversation: [
        {
          user: [{text:'Okay', val: 0}],
          zeus:'Hello there stranger. My name is Zeus and I\'m here to assist with tenant/landlord problems within Canada. I\'ll be going into beta soon.'
        },
        {
          user: [{text:'Sure', val: 0}, {text:'No Question', val: 1}],
          zeus:'Would you like to ask me a question? I\'ll email you the answer as soon as I can!'},
        {
          user: [{text:'Send', val: 3}],
          zeus:'Great! What is your question?'},
        {
          user: [{text:'Sure', val: 4}, {text:'No Thanks', val: 2}],
          zeus:'I\'ll keep your question in mind. Can I have your email? I\'ll send you the response ASAP!'},
        {
          user: [{text:'Okay', val: 0}],
          zeus:'Thanks! I\'ll be in touch!'}
      ],
      noQuestionConversation: [
        {
          user: [{text:'Sure', val: 0}, {text:'No', val: 2}],
          zeus:'Would you like to give us your email to know when I have my open beta?'},
        {
          user: [{text:'Okay', val: 0}],
          zeus:'Thanks! I\'ll be in touch!'}
      ],
      noEmailConversation: [
        {
          user: [{text:'Thanks', val: 0}],
          zeus:'Alright! Have a nice day.'
        }
      ],
      zeus: {
        input: null
      },
      user: {
        input: null,
        isSent: false,
      }
    }
  },
  created () {
    this.currentMap = this.regularConversation
    this.zeus.input = this.currentMap[this.counter].zeus
    this.user.inputs = this.currentMap[this.counter].user
  },
  methods: {
    // TODO Submit Email + Question
    sendUserMessage () {
      this.$http.post(this.api_url + 'conversation', {
      }).then(
        response => {
        },
        response => {
        }
      )
    },
    nextChat (item) {
      console.log(item)
      if (item === 1) {
        this.currentMap = this.noQuestionConversation
        this.counter = 0
      } else if (item === 2) {
        this.currentMap = this.noEmailConversation
        this.counter = 0
      } else {
        this.counter++
      }
      if (this.currentMap[this.counter] !== undefined){
        this.zeus.input = this.currentMap[this.counter].zeus
        this.user.inputs = this.currentMap[this.counter].user
        this.user.inputSize = 24/this.user.inputs
      } else {
        this.zeus.input = ":D"
        this.user.inputs = []
      }
    }
  }
}
</script>
