/*
import dependencies
*/

import Vue from 'vue'
import Dashboard from '@/components/Dashboard'
import ElementUI from 'element-ui'
import VueLocalStorage from 'vue-localstorage'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)

/*
test
*/

describe('Dashboard.vue', () => {

    it('should successfully set username', () => {
        const vm = new Vue(Dashboard).$mount()
        expect(Vue.localStorage.get('username')).to.be.equal('Patient Zero')
        Vue.localStorage.remove('username')
    })

})
