<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <b-container>
    <b-row>
      <b-col cols="12" sm="12">
        <div id="chat-component">
          <div id="chat-widow" v-chat-scroll>
            <div class="chat-message" v-for="(message, index) in chatLog">
              <div v-bind:class="{ 'chat-message-user': message.type == 'USER', 'chat-message-zeus': message.type == 'BOT' }">
                <img v-if="message.type == 'BOT'" src="../assets/bot.png"/>
                <p>{{ message.text }}</p>
              </div>
            </div>
          </div>
          <div id="chat-input">
            <input id="chat-input-text" type="textarea" v-model="currentUserInput"/>
            <button id="chat-input-submit" v-on:click="sendUserMessage" :disabled="!currentUserInput">Send</button>
            <icon id="chat-input-voice" name="microphone" scale="3"></icon>
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      chatLog: new Array,
      currentUserInput: null,
      username: null,
      connectionError: false
    }
  },
  created: function() {
    if (!this.$localStorage.get('zeusId')) {
      const zeusId = this.$localStorage.get('zeusId');
      this.getChatHistory(zeusId, this.initChat);
    } else {
      this.initChat();
    }
  },
  methods: {
    initChat: function() {
      this.chatLog.push({
        type: 'BOT',
        text: 'Hello there, I am ProceZeus, your personal legal assisstant. To get started, can you kindly tell me what is your name?'
      });
    },
    initChatSession: function() {
      this.$http.post('http://localhost:3003/new',{
        name: this.username
      }).then(response => {
        this.$localStorage.set('zeusId', response.body.conversation_id);
      }, response => {
        this.connectionError = true;
      });
    },
    sendUserMessage: function() {
      this.$http.post('http://localhost:3003/conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.currentUserInput
      }).then(response => {
        this.showMessage(this.currentUserInput, 'USER');
        this.showMessage(response.body.message, 'BOT');
      }, response => {
        this.connectionError = true;
      });
    },
    getChatHistory: function(zeusId, callback) {
      this.$http.get('http://localhost:3003/conversation/' + zeusId).then(response => {
        var chatHistory = response.body.message;
        for (var i = 0; i < chatHistory.length; i++) {
          this.showMessage(chatHistory[i].text, chatHistory[i].sender_type);
        }
        this.username = response.body.name;
      }, response => {
        callback();
      });
    },
    // push message to chatlog
    showMessage: function(text, type) {
      this.chatLog.push({
        text: text,
        type: type
      });
      if (type === 'USER') {
        this.currentUserInput = undefined;
      }
    }
  }
}
</script>
