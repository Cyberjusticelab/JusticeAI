<style lang="scss" scoped>
@import "../theme/Chat";
</style>

<template>
  <div id="chat-component">
    <!-- Chat History -->
    <transition name="fade">
      <div id="chat-history" v-if="user.openChatHistory" v-chat-scroll>
        <el-row>
          <el-col :sm="14">
            <div id="chat-container">
              <ul>
                <li v-for="conv in chatHistory">
                  <h3>{{ conv.sender_type }}</h3>
                  <p>- {{ conv.text }}</p>
                  <p>on {{ conv.timestamp.split('T')[0] }} at {{ conv.timestamp.split('T')[1].substring(0,8) }}</p>
                </li>
              </ul>
            </div>
          </el-col>
          <el-col :sm="2">
            <div id="previous-facts">
              <ul>
                <li>
                  <el-table
                    :data="tableData"
                    width="380">
                    <el-table-column
                      label="Statement"
                      width="120">
                      <template slot-scope="scope">
                        <el-popover trigger="hover" placement="top">
                          <p>{{ scope.row.description }}</p>
                          <div slot="reference">
                            <span style="margin-left: 10px">{{ scope.row.Fact_Summary }}</span>
                          </div>
                        </el-popover>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="Answer"
                      width="120">
                      <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.Answer }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column
                      label="Operations"
                      width="140">
                      <template slot-scope="scope">
                        <el-col>
                          <el-button
                            size="mini"
                            @click="handleEdit(scope.$index, scope.row)">Edit
                          </el-button>
                          <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">X
                          </el-button>
                        </el-col>
                      </template>
                    </el-table-column>
                  </el-table>
                </li>
              </ul>
            </div>
          </el-col>
          <el-col :sm="2">
            <div>&nbsp;</div>
          </el-col>
        </el-row>
      </div>
    </transition>
    <!-- End of Chat History -->
    <!-- Chat Widow -->
    <div id="chat-widow">
      <!-- Log out -->
      <div id="chat-nav">
        <el-row>
          <el-col :sm="2" :offset="22">
            <div id="chat-reset" v-on:click="resetChat()">
              <img alt="" src="../assets/logout.png">
              <p>
                <span v-if="isLoggedIn">Sign Out</span>
                <span v-if="!isLoggedIn">Reset</span>
              </p>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of Log out -->
      <!-- Zeus Chat -->
      <div id="chat-zeus-container">
        <el-row>
          <el-col :sm="4" :offset="3">
            <div id="chat-zeus-avatar">
              <img src="../assets/zeus_avatar_2.png"/>
            </div>
          </el-col>
          <el-col :sm="14">
            <div id="chat-message-zeus">
              <img v-if="!zeus.input" alt="" src="../assets/chatting.gif">
              <transition name="fade">
                <div>
                  <div v-if="zeus.enableUserConfirmation">
                    <p>Did I understand you correctly?</p>
                    <div v-if="factType === 'boolean'">
                      <button v-on:click="confirmBotResponse(true)">Yes</button>
                      <button v-on:click="confirmBotResponse(false)">No</button>
                    </div>
                    <div v-if="factType !== 'boolean'">
                      <input type="text" v-model="userConfirmationText"/>
                      <button v-on:click="confirmBotResponse(userConfirmationText)">OK</button>
                    </div>
                  </div>
                  <p v-if="zeus.input" v-html="zeus.input"></p>
                </div>
              </transition>
              <transition name="fade">
                <file-upload
                  ref="upload"
                  v-model="zeus.file"
                  :drop="true"
                  :post-action="uploadUrl"
                  v-if="zeus.filePrompt"
                  extensions="jpg,jpeg,pdf,docx,webp,png"
                >
                  <p v-if="zeus.file.length == 0" id="drag-and-drop">drag and drop or click to select file</p>
                  <p v-if="zeus.file" id="file-name" v-for="file in zeus.file">{{ file.name }}</p>
                </file-upload>
              </transition>
              <div id="file-upload-button-group" v-if="zeus.filePrompt">
                <el-button v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true" type="warning" :disabled="zeus.file.length == 0">
                  Upload
                </el-button>
                <el-button v-show="$refs.upload && $refs.upload.active" @click.prevent="$refs.upload.active = false" type="warning">
                  Stop
                </el-button>
                <p v-if="zeus.file[0] && zeus.file[0].success && $refs.upload.uploaded">
                  Successfully uploaded <span>{{ zeus.file[0].name }}</span>
                </p>
              </div>
              <div id="pre-selected-answer-group" v-if="zeus.suggestion && zeus.input">
                <el-button v-for="answer in zeus.suggestion" :key="answer.id" type="warning" v-on:click="user.input = answer; sendUserMessage()">
                  {{ answer }}
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of Zeus Chat -->
      <!-- User Chat -->
      <div id="chat-user-container">
        <el-row>
          <el-col :sm="14" :offset="3">
            <div id="chat-message-user" v-bind:class="{ msgIsSent: user.isSent && chatHistory}">
              <img v-if="!user.input" alt="" src="../assets/chatting.gif">
              <p v-if="user.input" v-html="user.input"></p>
            </div>
          </el-col>
          <el-col :md="4">
            <div id="chat-user-avatar">
              <img src="../assets/user_avatar_2.png"/>
            </div>
          </el-col>
        </el-row>
      </div>
      <!-- End of User Chat -->
    </div>
    <!-- End of Chat Widow -->
    <!-- Input Widow -->
    <div id="chat-input">
      <form v-on:submit.prevent="sendUserMessage()">
        <el-input id="chat-input-text" autosize v-model="user.input" placeholder="Enter your message" autoComplete="off" :disabled="user.disableInput"></el-input>
        <el-button id="chat-input-submit" type="warning" :disabled="!user.input" native-type="submit">SEND</el-button>
        <div id="chat-history-button" v-on:click="user.openChatHistory = !user.openChatHistory; getChatHistory()">
          <img v-if="!user.openChatHistory" alt="" src="../assets/history_open.png">
          <img v-if="user.openChatHistory" alt="" src="../assets/history_disable.png">
        </div>
      </form>
      <!--<icon id="chat-input-voice" name="microphone" scale="3"></icon>-->
    </div>
    <!-- End of Input Widow -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      api_url: process.env.API_URL,
      uploadUrl: new String,
      connectionError: false,
      chatHistory: new Array,
      numMessageSinceChatHistory: 0,
      isLoggedIn: false, //TODO: account feature
      factType: 'boolean',
      zeus: {
        input: null,
        file: new Array,
        filePrompt: false,
        enableUserConfirmation: false,
        suggestion: new Array
      },
      user: {
        name: null,
        input: null,
        isSent: false,
        openChatHistory: false,
        disableInput: false
      },
      tableData: [{
        Fact_Summary: 'Fact 1',
        Answer: 'Answer 1',
        description: 'Description 1'
      }, {
        Fact_Summary: 'Fact 2',
        Answer: 'Answer 2',
        description: 'Description 2'
      }, {
        Fact_Summary: 'Fact 3',
        Answer: 'Answer 3',
        description: 'Description 3'
      }, {
        Fact_Summary: 'Fact 4',
        Answer: 'Answer 4',
        description: 'Description 4'
      }]
    }
  },
  created() {
    if (this.$localStorage.get('zeusId')) {
      this.getChatHistory()
    } else {
      this.initChatSession()
    }
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    initChatSession() {
      this.$http.post(this.api_url + 'new', {
        name: this.$localStorage.get('username'),
        person_type: this.$localStorage.get('usertype')
      }).then(
        response => {
          this.$localStorage.set('zeusId', response.body.conversation_id)
          this.user.input = ''
          this.sendUserMessage()
          this.uploadUrl = this.api_url + 'conversation/' + response.body.conversation_id + '/files'
        },
        response => {
          this.connectionError = true
        }
      )
    },
    sendUserMessage() {
      this.$http.post(this.api_url + 'conversation', {
        conversation_id: this.$localStorage.get('zeusId'),
        message: this.user.input
      }).then(
        response => {
          this.zeus.input = null
          this.user.isSent = this.user.input != ''
          this.zeus.filePrompt = false;
          this.numMessageSinceChatHistory += 1
          setTimeout(() => {
            this.configChat(response.body)
          }, 1100)
        },
        response => {
          this.connectionError = true
        }
      )
    },
    getChatHistory() {
      let zeusId = this.$localStorage.get('zeusId')
      this.$http.get(this.api_url + 'conversation/' + zeusId).then(
        response => {
          this.chatHistory = response.body.messages
          this.numMessageSinceChatHistory = 0
          this.user.name = response.body.name
          if (!this.zeus.input) {
            this.configChat(this.chatHistory[this.chatHistory.length - 1])
          }
          this.uploadUrl = this.api_url + 'conversation/' + zeusId + '/files'
          this.setEnableUserConfirmation()
        },
        response => {
          this.connectionError = true
        }
      )
    },
    configChat(conversation) {
      this.zeus.input = conversation.message || conversation.html || conversation.text
      this.zeus.filePrompt = (conversation.file_request !== undefined) && (conversation.file_request !== null)
      if (conversation.possible_answers == undefined) {
        this.zeus.suggestion = []
      } else {
        this.zeus.suggestion = JSON.parse(conversation.possible_answers) || []
      }
      this.numMessageSinceChatHistory += 1
      this.setEnableUserConfirmation()
      this.factType = conversation.fact_type || 'boolean'
      this.user.input = null
      this.user.isSent = false
      this.user.disableInput = conversation.enforce_possible_answer
    },
    confirmBotResponse(confirmation) {
      this.$http.post(this.api_url + 'store-user-confirmation', {
        conversation_id: this.$localStorage.get('zeusId'),
        confirmation: confirmation || false
      }).then(response => {
        this.zeus.enableUserConfirmation = false
      }, response => {
        this.zeus.enableUserConfirmation = true
        this.connectionError = true
      })
    },
    setEnableUserConfirmation() {
      // Only start prompting once user has start responding to questions
      this.zeus.enableUserConfirmation = this.numMessageSinceChatHistory + this.chatHistory.length > 4
    },
    resetChat() {
      if (this.isLoggedIn) {
        //TODO: some logout logic here
      } else {
        this.$localStorage.remove('zeusId')
        this.$localStorage.remove('username')
        this.$localStorage.remove('usertype')
        this.$router.push('/')
      }
    }
  }
}
</script>
