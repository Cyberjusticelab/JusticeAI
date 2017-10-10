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
      this.chatLog.push({
        type: 'user',
        text: this.currentUserInput
      });
      this.currentUserInput = undefined;
    }
  }
}
</script>

<style lang="scss" scoped>
#chat-widow {
  margin-top: 20px;
  height: 800px;
  border: 1px solid #000000;
  overflow-y: scroll;
  .chat-message {
    height: 20px;
    margin: 20px 20px 0px 20px;
    font-size:35px;
  }
  .chat-message-user {
    @extend .chat-message;
    margin-top: 36px;
    text-align: right;
  }
  .chat-message-zeus {
    @extend .chat-message;
    text-align: left;
    img {
      width: 60px;
      margin-right: 20px;
      display: inline-block;
    }
    p {
      display: inline-block;
    }
  }
}
#chat-input {
  margin-top: 20px;
  #chat-input-text {
    width: 500px;
    height: 50px;
    padding: 2px 20px 2px 20px;
  }
  #chat-input-submit {
    height: 58px;
    width: 110px;
  }
  #chat-input-voice {
    margin: 0px 0px -18px 20px;
  }
}
</style>
