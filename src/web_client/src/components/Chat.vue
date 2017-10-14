<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <b-container fluid id="chat-component">
    <b-row id="chat-title">
      <b-col sm="2"><h2>ProceZeus</h2></b-col>
    </b-row>
    <div id="chat-widow" v-chat-scroll>
      <div class="chat-message-container" v-for="(message, index) in chatLog">
        <b-row>
          <b-col sm="3" offset-sm="1">
            <div v-if="message.type == 'BOT'" class="chat-message-img">
              <img src="../assets/zeus.jpg"/>
            </div>
          </b-col>
          <b-col sm="8">
            <div v-bind:class="{ 'chat-message-user': message.type == 'USER', 'chat-message-zeus': message.type == 'BOT' }" class="chat-message-text">
              <p>{{ message.text }}</p>
            </div>
          </b-col>
        </b-row>
      </div>
    </div>
    <div id="chat-input">
      <b-form @submit="sendUserMessage">
        <b-form-group>
          <b-form-input id="chat-input-text" v-model="currentUserInput" placeholder="Enter your message" autocomplete="off"></b-form-input>
          <b-button id="chat-input-submit" size="lg" variant="outline-success" type="submit":disabled="!currentUserInput">Send</b-button>
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
          this.showMessage(this.currentUserInput, 'USER');
          this.showMessage(response.body.message, 'BOT');
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    getChatHistory (zeusId) {
      this.$http.get('http://localhost:3003/conversation/' + zeusId).then(
        response => {
          let chatHistory = response.body.messages;
          for (let i = 0; i < chatHistory.length; i++) {
            this.showMessage(chatHistory[i].text, chatHistory[i].sender_type);
          }
          this.username = response.body.name;
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    showMessage (text, type) {
      if (text) {
        this.chatLog.push({
          text: text,
          type: type
        });
      }
      if (type === 'USER') {
        this.currentUserInput = undefined;
      }
    }
  }
}
</script>
