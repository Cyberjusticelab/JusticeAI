import Vue from 'vue'
import ProceZeus from './ProceZeus'
import router from './router'
import VueChatScroll from 'vue-chat-scroll'

Vue.config.productionTip = false
Vue.use(VueChatScroll)

/* eslint-disable no-new */
new Vue({
  el: '#proceZeus',
  router,
  render: h => h(ProceZeus)
})

