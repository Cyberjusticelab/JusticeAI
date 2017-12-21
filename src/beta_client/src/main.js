import Vue from 'vue'
import ProceZeus from './ProceZeus'
import router from './router'
import VueResource from 'vue-resource'
import VueChatScroll from 'vue-chat-scroll'
import ElementUI from 'element-ui'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(VueChatScroll)
Vue.use(ElementUI)
Vue.component('icon', Icon)

/* eslint-disable no-new */
new Vue({
  el: '#proceZeus',
  router,
  render: h => h(ProceZeus)
})

