/*
import dependencies
*/

import Vue from 'vue'
import Dashboard from '@/components/Dashboard'
import ElementUI from 'element-ui'
import VueLocalStorage from 'vue-localstorage'
import {EventBus} from '@/components/EventBus.js'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)

/*
test
*/

describe('Dashboard.vue', () => {

  it('should successfully listen to event', () => {
    const vm = new Vue(Dashboard).$mount()
    EventBus.$emit('initLoading', true)
    expect(vm.initLoading).to.equal(true)
  })

})
