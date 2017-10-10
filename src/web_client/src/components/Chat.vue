<template>
  <div id="chat-component">
    <div id="chat-widow" v-chat-scroll>
      <div class="chat-message" v-for="(message, index) in chatLog">
        <div v-bind:class="{ 'chat-message-user': message.type == 'user', 'chat-message-zeus': message.type == 'zeus' }">
          <img v-if="message.type == 'zeus'" src="../assets/bot.png"/>
          <p>{{ message.text }}</p>
        </div>
      </div>
    </div>
    <div id="chat-window-bottom"></div>
    <div id="chat-input">
      <input type="textarea" v-model="currentUserInput"/>
      <button v-on:click="sendUserMessage" :disabled="!currentUserInput">Send</button>
      <button>Voice</button>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      chatLog: [
        {
          type: 'zeus',
          text: 'HI!'
        }
      ],
      currentUserInput: ''
    }
  },
  methods: {
    sendUserMessage: function() {
      this.chatLog.push({
        type: 'user',
        text: this.currentUserInput
      });
      this.currentUserInput = '';
    }
  }
}
</script>

<style scoped>
#chat-widow {
  height: 800px;
  border: 1px solid black;
  overflow-y: scroll;
}
.chat-message-user {
  height: 20px;
  text-align: right;
  margin: 0px 20px 0px 20px;
}
.chat-message-zeus {
  height: 20px;
  text-align: left;
  margin: 0px 20px 0px 20px;
}
.chat-message-zeus img {
  width: 20px;
  display: inline-block;
}
.chat-message-zeus p {
  display: inline-block;
}
</style>
