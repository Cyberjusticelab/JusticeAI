<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <b-container fluid id="chat-component">
    <div id="chat-widow">
      <!--
      <div class="chat-message-container" v-for="(message, index) in chatLog">
        <b-row>
          <b-col sm="3" offset-sm="1">
            <div v-if="message.type == 'BOT'" class="chat-message-img">
              <img src="../assets/zeus_avatar_2.png"/>
            </div>
          </b-col>
          <b-col sm="8">
            <div v-bind:class="{ 'chat-message-user': message.type == 'USER', 'chat-message-zeus': message.type == 'BOT' }" class="chat-message-text">
              <p>{{ message.text }}</p>
            </div>
          </b-col>
        </b-row>
      </div>
      -->
      <div id="logout">
        <b-row>
          <b-col md="2" offset-md="10">
            <img alt="" src="../assets/logout.png">
            <p>LOG OUT</p>
          </b-col>
        </b-row>
      </div>
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
      <div id="chat-user-container">
        <b-row>
          <b-col md="7" offset-md="2">
            <div id="chat-message-user">
              <img v-if="!currentUserInput" alt="" src="../assets/chatting.gif">
              <p v-if="currentUserInput">{{ currentUserInput }}</p>
            </div>
          </b-col>
          <b-col md="2">
            <div id="chat-user-avatar">
              <img src="../assets/user_avatar_2.png"/>
            </div>
          </b-col>
        </b-row>
      </div>
    </div>
    <div id="chat-input">
      <b-form @submit.prevent="sendUserMessage()">
        <b-form-group>
          <b-form-input id="chat-input-text" v-model="currentUserInput" placeholder="Enter your message" autocomplete="off"></b-form-input>
          <b-button id="chat-input-submit" size="lg" variant="outline-success" type="submit":disabled="!currentUserInput">SEND</b-button>
        </b-form-group>
      </b-form>
      <!--<icon id="chat-input-voice" name="microphone" scale="3"></icon>-->
    </div>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      chatLog: new Array,
      currentUserInput: null,
      currentZeusInput: null,
      username: 'Hammer of Justice!', // TODO: prompt user's name
      connectionError: false
    }
  },
  created () {
    if (this.$localStorage.get('zeusId')) {
      let zeusId = this.$localStorage.get('zeusId');
      this.getChatHistory(zeusId);
    } else {
      this.initChatSession();
    }
  },
  methods: {
    initChatSession () {
      this.$http.post('http://localhost:3003/new',{
        name: this.username
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
      this.$http.post('http://localhost:3003/conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.currentUserInput
      }).then(
        response => {
          this.currentZeusInput = response.body.message;
          this.currentUserInput = null;
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    getChatHistory (zeusId) {
      this.$http.get('http://localhost:3003/conversation/' + zeusId).then(
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
