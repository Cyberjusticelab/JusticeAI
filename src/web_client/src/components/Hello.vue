<template>
  <div>
    <div class="welcome">
      <img src="../assets/logo.svg" v-bind:class="{ 'logo': !startChat, 'logo-reduced': startChat }">
      <div class="landing" v-if="!startChat">
        <h1>{{ landingPageTitle }}</h1>
        <p>{{ landingPageMessage }}</p>
        <p>{{ landingPagePrompt }}</p>
      </div>
      <div id="conversation" class="conversation" v-if="startChat">
        <div class="conversationLine">
          <div class="botMessageBlock">
            <p class="botMessage">{{ botMessageLog[0] }}</p>
          </div>
          <div class="botAvatarBlock">
            <img class="avatar" src="../assets/bot.png">
            <div class="botName">{{ botName }}</div>
          </div>
        </div>
        <div v-for="(userMessage, index) in userMessageLog">
          <div class="conversationLine">
            <div class="userAvatarBlock">
              <img class="avatar" src="../assets/user.png">
              <div class="avatarName">{{ username }}</div>
            </div>
            <div class="userMessageBlock">
              <p class="userMessage">{{ userMessage }}</p>
            </div>
          </div>
          <div class="conversationLine">
            <div class="botMessageBlock">
              <p class="botMessage">{{ botMessageLog[index+1] }}</p>
            </div>
            <div class="botAvatarBlock">
              <img class="avatar" src="../assets/bot.png">
              <div class="botName">{{ botName }}</div>
            </div>
          </div>
        </div>
        <div id="bottomOfConversation"></div>
      </div>
      <div v-if="!startChat">
        <input type="text" v-model="username"/>
        <div>
          <button v-on:click="openChatBot">Get Started!</button>
        </div>
      </div>

    </div>
    <div class="userTextBoxDiv" v-if="startChat">
      <textarea class="userTextBox" v-model="userTextInput"></textarea>
      <button class="userTextSubmit" v-on:click="submitUserText">Submit</button>
    </div>
  </div>
</template>

<script>
const VueScrollTo = require('vue-scrollto');
export default {
  name: 'welcome',
  data () {
    return {
      landingPageTitle: 'Hi! I\'m ProceZeus.',
      landingPageMessage: 'I\'m a bot that can help you navigate the resolution of a dispute between a landlord and a tenant.',
      landingPagePrompt: 'First, let\'s get to know each other. What\'s your name?',
      startChat: false,
      botName: "ProceZeus",
      botMessageLog: [],
      userMessageLog: []
    }
  },
  methods: {
    openChatBot: function() {
      if (this.username.trim()) {
        this.startChat = true;
        this.botMessageLog.push("Hi " + this.username + "! How can I help you today?")
      }
    },
    submitUserText: function() {
      if (this.userTextInput.trim()) {
        this.userMessageLog.push(this.userTextInput);
        this.userTextInput = "";
        this.botMessageLog.push("This is a default response until NLP/ML logic is implemented.");
        const scrollOptions = {
            container: '#conversation',
            easing: 'ease-in',
            offset: -60,
            cancelable: true,
            onDone: function() {
              // scrolling is done
            },
            onCancel: function() {
              // scrolling has been interrupted
            },
            x: false,
            y: true
        }
        VueScrollTo.scrollTo('#bottomOfConversation', 600, scrollOptions);
      }
    }
  }
}
</script>
<style scoped>
.welcome {
  min-height: 100%;
}
.logo {
  height: 250px;
  margin-top: 100px;
  -webkit-transition: height 0.5s; /* Safari */
  transition: height 0.5s;
}
.logo-reduced {
  height: 80px;
  margin-top: 30px;
  -webkit-transition: height 0.5s; /* Safari */
  transition: height 0.5s;
}
.landing h1 {
  font-size: 45px;
}
.landing p {
  font-size: 25px;
}
input {
  width: 80%;
  max-width: 500px;
  font-size: 20px;
  padding: 15px;
}
button {
  border: none;
  border-radius: 5px;
  width: 185px;
  background-color: #5196C3;
  color: #ffffff;
  font-weight: bold;
  padding: 15px;
  font-size: 25px;
  margin: 30px 0;
}
button:hover{
  border: 1px, solid, #5196c3;
  background-color: #61A6D3;
}
#conversation {
  width: 70%;
  margin: 30px auto;
  padding: 30px;
  border-radius: 10px;
  max-height: 500px;
  overflow-y: auto;
}
::-webkit-scrollbar {
    width: 0px;
    background: transparent;
}
.userAvatarBlock {
  display: inline-block;
  float: right;
}
.botAvatarBlock {
  display: inline-block;
  float: left;
}
.avatar {
  height: 50px;
  width: 50px;
}
.avatarName {
  width: 80px;
  text-align: center;
  font-size: 20px;
}
.usermessageBlock {
  position: relative;
  left: 100px;
}
.conversationLine {
  display: block;
  border-radius: 5px;
  background-color: rgba(0,0,0,0.15);
  overflow: hidden;
  margin: 10px 0;
  padding: 10px;
}
.botMessage {
  margin-top: 30px;
  font-size: 20px;
  text-align: left;
}
.userMessage {
  margin-top: 30px;
  font-size: 20px;
  text-align: right;
}
.botMessageBlock {
  display: block;
  float: right;
  width: calc(100% - 100px);
}
.userMessageBlock {
  display: block;
  float: left;
  width: calc(100% - 100px);
}
.userTextBoxDiv {
  position: absolute;
  bottom: 0;
  height: 200px;
  width: 100%;
}
.userTextBox {
  display: block;
  margin: 0 auto;
  height: 50px;
  width: 60%;
  min-width: 200px;
  padding: 20px;
  border-radius: 5px;
  font-size: 16px;
  color: #222222;
}
.userTextSubmit{
  margin: 10px;
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
