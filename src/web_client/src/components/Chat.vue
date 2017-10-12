<template>
  <b-container>
    <b-row>
      <b-col cols="12" sm="10">
        <div id="chat-component">
          <div id="chat-widow" v-chat-scroll>
            <div class="chat-message" v-for="(message, index) in chatLog">
              <div v-bind:class="{ 'chat-message-user': message.type == 'user', 'chat-message-zeus': message.type == 'zeus' }">
                <img v-if="message.type == 'zeus'" src="../assets/bot.png"/>
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
      currentUserInput: undefined
    }
  },
  created: function() {
    //TODO: init session
    this.chatLog.push({
      type: 'zeus',
      text: 'HI!'
    });
  },
  methods: {
    sendUserMessage: function() {
      // TODO: request to APIs to send the message first, then do callback to push the object
      this.$http.get('http://www.whatever.com').then(response => {
        this.zeusResponse = response.body;
        this.showMessage(this.currentUserInput, 'user');
        // TODO: push zeus message to chatlog
        // TODO: play around with the data
        console.log(this.zeusResponse);
      }, response => {
        this.showMessage(this.currentUserInput, 'user');
        // error callback
      });
    },
    showMessage: function(text, type) {
      this.chatLog.push({
        text: text,
        type: type
      });
      if (type === 'user') {
        this.currentUserInput = undefined;
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../theme/Chat"
</style>
