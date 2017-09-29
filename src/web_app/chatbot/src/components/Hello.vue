<template>
  <div class="welcome">
    <div class="landing" v-if="!startChat">
      <h1>{{ msg }}</h1>
    </div>
    <div class="conversation" v-if="startChat">
      <div class="convBlock">
        <img class="avatar" src="../assets/user.png">
        <p class="conversationMsg">{{ userMsg }}</p>
      </div>
      <div class="convBlock">
        <img class="avatar" src="../assets/bot.png">
        <p class="conversationMsg">{{ aiMsg }}</p>
      </div>
    </div>
    <div><input type="text" v-model="userMsg"/></div>
    <button v-on:click="openChatBot">Start</button>
  </div>
</template>

<script>
export default {
  name: 'welcome',
  data () {
    return {
      msg: 'Welcome to proceZeus! To get started, please tell us what you’d like to do.',
      startChat: false,
      aiMsg: 'Hello, I am proceZeus. Please let me take a look at your case.'
    }
  },
  methods: {
    openChatBot: function() {
      this.startChat = true;
    }
  }
}
</script>
<style scoped>
h1 {
  font-weight: normal;
  font-size: 20px;
}
input {
  width: 400px;
  height: 25px;
  font-size: 20px;
  padding: 15px;
}
button {
  border: none;
  margin-top: 10px;
  width: 185px;
  height: 30px;
  background-color: #5196C3;
  color: #ffffff;
  font-size: 14px;
  font-weight: bold;
}
button:hover{
  border-style: groove;
  border: 1px, solid, #5196c3;
  background-color: #ffffff;
  color: #5196C3;
}
.avatar {
  height: 70px;
}
.conversation {
  margin-bottom: 30px;
}
.conversationMsg {
  display: inline-block;
  margin-left: 50px;
  position: absolute;
  padding-top: 10px
}
.convBlock {
  width: 70%;
  margin: auto;
  margin-top: 10px;
  text-align: left;
}
</style>
