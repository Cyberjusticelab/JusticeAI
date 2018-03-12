import Vue from 'vue'
import ProceZeus from './ProceZeus'
import router from './router'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
import VueUpload from 'vue-upload-component'
import VueChart from 'vuechart';
import ElementUI from 'element-ui'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(VueLocalStorage)
Vue.use(ElementUI)
Vue.component(VueChart.name, VueChart);
Vue.component('icon', Icon)
Vue.component('file-upload', VueUpload)

/* eslint-disable no-new */
new Vue({
  el: '#proceZeus',
  router,
  render: h => h(ProceZeus)
})

