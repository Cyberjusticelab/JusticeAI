<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <b-container fluid id="chat-component">
    <!-- Chat History -->
    <transition name="fade">
      <div id="chat-history" v-if="openChatHistory" v-chat-scroll>
        <ul>
          <li v-for="conv in chatLog">
            <h3>{{ conv.sender_type }}</h3>
            <p>- {{ conv.text }}</p>
            <p>on {{ conv.timestamp.split('T')[0] }} at {{ conv.timestamp.split('T')[1].substring(0,8) }}</p>
          </li>
        </ul>
      </div>
    </transition>
    <!-- End of Chat History -->
    <!-- Chat Widow -->
    <div id="chat-widow">
      <!-- Log out -->
      <div id="logout">
        <b-row>
          <b-col md="2" offset-md="10">
            <img alt="" src="../assets/logout.png">
            <p>LOG OUT</p>
          </b-col>
        </b-row>
      </div>
      <!-- End of Log out -->
      <!-- Zeus Chat -->
      <div id="chat-zeus-container">
        <b-row>
          <b-col md="2" offset-md="1">
            <div id="chat-zeus-avatar">
              <img src="../assets/zeus_avatar_2.png"/>
            </div>
          </b-col>
          <b-col md="7">
            <div id="chat-message-zeus">
              <img v-if="!currentZeusInput" alt="" src="../assets/chatting.gif">
              <transition name="fade">
                <p v-if="currentZeusInput">{{ currentZeusInput }} </p>
              </transition>
            </div>
          </b-col>
        </b-row>
      </div>
      <!-- End of Zeus Chat -->
      <!-- User Chat -->
      <div id="chat-user-container">
        <b-row>
          <b-col md="7" offset-md="2">
            <div id="chat-message-user">
              <img v-if="!currentUserInput" alt="" src="../assets/chatting.gif">
              <p v-if="currentUserInput">{{ currentUserInput }}</p>
            </div>
          </b-col>
          <b-col md="1">
            <div id="chat-user-avatar">
              <img src="../assets/user_avatar_2.png"/>
            </div>
          </b-col>
        </b-row>
      </div>
      <!-- End of User Chat -->
    </div>
    <!-- End of Chat Widow -->
    <!-- Input Widow -->
    <div id="chat-input">
      <b-form @submit.prevent="sendUserMessage()">
        <b-form-group>
          <b-form-input id="chat-input-text" v-model="currentUserInput" placeholder="Enter your message" autocomplete="off"></b-form-input>
          <b-button id="chat-input-submit" size="lg" variant="outline-success" type="submit":disabled="!currentUserInput">SEND</b-button>
          <div id="chat-history-button" v-on:click="openChatHistory = !openChatHistory; getChatHistory()">
            <img v-if="!openChatHistory" alt="" src="../assets/history_open.png">
            <img v-if="openChatHistory" alt="" src="../assets/history_disable.png">
          </div>
        </b-form-group>
      </b-form>
      <!--<icon id="chat-input-voice" name="microphone" scale="3"></icon>-->
    </div>
    <!-- End of Input Widow -->
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      chatLog: new Array,
      currentUserInput: null,
      currentZeusInput: null,
      username: null,
      connectionError: false,
      openChatHistory: false,
      api_url: process.env.API_URL
    }
  },
  created () {
    if (this.$localStorage.get('zeusId')) {
      this.getChatHistory();
    } else {
      this.initChatSession();
    }
  },
  methods: {
    initChatSession () {
      this.$http.post(this.api_url + 'new',{
        name: this.$localStorage.get('username')
      }).then(
        response => {
          this.$localStorage.set('zeusId', response.body.conversation_id);
          this.currentUserInput = '';
          this.sendUserMessage();
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    sendUserMessage () {
      this.$http.post(this.api_url + 'conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.currentUserInput
      }).then(
        response => {
          this.currentZeusInput = null;
          setTimeout(() => {
            this.currentZeusInput = response.body.message;
            this.currentUserInput = null;
          }, 800);
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    getChatHistory () {
      let zeusId = this.$localStorage.get('zeusId');
      this.$http.get(this.api_url + 'conversation/' + zeusId).then(
        response => {
          this.chatLog = response.body.messages;
          this.username = response.body.name;
          if (!this.currentZeusInput) {
            this.currentZeusInput = this.chatLog[this.chatLog.length-1].text;
          }
        },
        response => {
          this.connectionError = true;
        }
      );
    }
  }
}
</script>
