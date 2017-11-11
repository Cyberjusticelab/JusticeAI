/*
import dependencies
*/

import Vue from 'vue'
import Landing from '@/components/Landing'
import ElementUI from 'element-ui'
import VueLocalStorage from 'vue-localstorage'
import VueRouter from 'vue-router'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueRouter)

/*
test
*/

describe('Landing.vue', () => {

    it('should resume chat if conversation id exists', () => {
    	Vue.localStorage.set('zeusId', 1)
        const Component = Vue.extend(Landing)
    	const vm = new Component({
    		router: new VueRouter({
    			routes: [
    				{
    					path: '/dashboard',
    					name: 'dashboard'
    				}
    			]
    		})
    	}).$mount()
    	Vue.localStorage.remove('zeusId')
    })

    it('should choose user type', () => {
    	const Component = Vue.extend(Landing)
    	const vm = new Component({
    		router: new VueRouter({
    			routes: [
    				{
    					path: '/dashboard',
    					name: 'dashboard'
    				}
    			]
    		})
    	}).$mount()
    	vm.chooseType('tenant')
    	expect(Vue.localStorage.get('username')).to.be.equal('tenant')
    	expect(Vue.localStorage.get('usertype')).to.be.equal('tenant')
    })

})
