import Vue from 'vue'
import ProceZeus from './ProceZeus'
import router from './router'
import VueChatScroll from 'vue-chat-scroll'
import BootstrapVue from 'bootstrap-vue'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false
Vue.use(VueChatScroll)
Vue.use(BootstrapVue)
Vue.component('icon', Icon)

/* eslint-disable no-new */
new Vue({
  el: '#proceZeus',
  router,
  render: h => h(ProceZeus)
})

