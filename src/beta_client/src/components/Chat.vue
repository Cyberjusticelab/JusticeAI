<style lang="scss" scoped>
@import "../theme/Chat"
</style>

<template>
  <div id="chat-component">
      <div id="chat-zeus-container">
        <el-row>
          <el-col :sm="{span: 4, offset: 1}" :xs="{span: 24}">
            <div id="chat-zeus-avatar">
              <img src="../assets/zeus_avatar_2.png"/>
            </div>
          </el-col>
          <el-col :sm="{span: 18}" :xs="{span: 22, offset: 1}">
            <div id="chat-message-zeus">
              <div>
                <p v-if="currentConversation" v-html="currentConversation.zeus"></p>
              </div>
            </div>
          </el-col>
        </el-row>
    </div>
    <div id="chat-input">
      <el-row>
        <div v-for="answer in currentConversation.user">
          <el-col v-if="answer.type=='question' || answer.type=='email'" :sm="24">
            <el-input v-if="answer.type=='question'" autosize v-model="userQuestion" placeholder="ENTER YOUR QUESTION" autoComplete="off"></el-input>
            <el-input v-if="answer.type=='email'" autosize v-model="userEmail" placeholder="ENTER YOUR EMAIL"></el-input>
          </el-col>
          <el-col :sm="colSize">
            <el-button type="warning" v-on:click="validateAnswer(answer)">{{answer.text}}</el-button>
          </el-col>
        </div>
      </el-row>
      <el-row>
        <transition name="fade">
          <p id="invalid-answer" v-if="isInvalidInput">Please make sure your input is valid and not empty, thanks!</p>
        </transition>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chat',
  data () {
    return {
      api_url: process.env.API_URL,
      conversation: [
        {
          user: [{text:'Okay', val: 1}],
          zeus:'Hello there stranger! My name is Zeus and I\'m here to assist you with your Québec tenant/landlord issues. I\'ll be going into beta soon, and would like to get more context about common problems. If you don\'t mind telling me about any tenant/landlord issues you have, we\'ll try to get back to you as soon as possible with some useful information.'
        },
        {
          user: [{text:'Sure', val: 2}, {text:'I have no question', val: 3}],
          zeus:'Would you like to ask me a question about tenant/landlord issue?'
        },
        {
          user: [{text:'Confirm', val: 3, type: 'question'}],
          zeus:'Great! What is your question?'
        },
        {
          user: [{text:'Confirm', val: 4, type: 'email'}],
          zeus:'Mind leaving your email so that we can let you know once our beta is live?'
        },
        {
          user: [{text:'Sure', val: 5, type: 'subscription'}, {text:'No, thanks', val: 5}],
          zeus:'Would you like to receive updates on our beta test?'
        },
        {
          user: [{text:'Close', val: -1}],
          zeus:'Thank you so much! I\'ll be in touch. Have a nice day!'
        }
      ],
      colSize: 24,
      currentConversation: null,
      userEmail: null,
      userQuestion: null,
      userSubscription: false,
      userId: null,
      isInvalidInput: false
    }
  },
  created () {
    this.currentConversation = this.conversation[0]
  },
  methods: {
    validateAnswer (item) {
      this.isInvalidInput = false
      if (item.type === 'question') {
        if (this.userQuestion) {
          this.$http.post(this.api_url + 'question', {
            question: this.userQuestion
          }).then(
            response => {
              userId = response.data.id
            }
          )
        } else {
          this.isInvalidInput = true
        }
      } else if (item.type === 'email') {
        if (/^.+@[a-zA-Z0-9\-]+\.[a-zA-Z]+$/.test(this.userEmail)) {
          this.$http.put(this.api_url + 'email', {
            id: this.userId,
            email: this.userEmail
          })
        } else {
          this.isInvalidInput = true
        }
      } else if (item.type === 'subscription') {
        this.$http.put(this.api_url + 'subscription', {
          id: this.userId,
          is_subscribed: 1
        })
      } else if (item.val == -1) {
        this.$router.go('/')
      }
      if (!this.isInvalidInput) {
        this.currentConversation = this.conversation[item.val];
        this.colSize = 24/this.currentConversation.user.length;
      }
    }
  }
}
</script>
