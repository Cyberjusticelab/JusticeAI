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
      username: 'Hammer of Justice', // TODO: prompt user's name
      connectionError: false
    }
  },
  created: function() {
    if (!this.$localStorage.get('zeusId')) {
      let zeusId = this.$localStorage.get('zeusId');
      this.getChatHistory(zeusId);
    } else {
      this.initChatSession();
    }
  },
  methods: {
    initChatSession() {
      this.$http.post('http://localhost:3003/new',{
        name: this.username
      }).then(
        response => {
          this.$localStorage.set('zeusId', response.body.conversation_id);
          sendUserMessage('');
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    sendUserMessage(message) {
      let userMessage = message || this.currentUserInput;
      this.$http.post('http://localhost:3003/conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: userMessage
      }).then(
        response => {
          this.shwoMessage(this.currentUserInput, 'USER');
          this.showMessage(response.body.message, 'BOT');
        },
        response => {
          this.connectionError = true;
        }
      );
    },
    getChatHistory(zeusId) {
      this.$http.get('http://localhost:3003/conversation/' + zeusId).then(
        response => {
          let chatHistory = response.body.message;
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
    // push message to chatlog
    showMessage(text, type) {
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
