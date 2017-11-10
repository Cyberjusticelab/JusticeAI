/*
import dependencies
*/

import Vue from 'vue'
import Chat from '@/components/Chat'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueResource)

/*
test
*/

describe('Chat.vue', () => {

    it('should resume chat session', () => {
    	Vue.localStorage.set('zeusId', 1)
    	const spy = sinon.spy(Chat.methods, "getChatHistory")
        const vm = new Vue(Chat).$mount()
        expect(spy.called).to.be.true
        Chat.methods.getChatHistory.restore()
        Vue.localStorage.remove('zeusId')
    })

    it('should init new chat session', () => {
    	const spy = sinon.spy(Chat.methods, "getChatHistory")
        const vm = new Vue(Chat).$mount()
        expect(spy.called).to.be.false
        Chat.methods.getChatHistory.reset()
    })

})
