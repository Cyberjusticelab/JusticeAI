/*
import dependencies
*/

import Vue from 'vue'
import Chat from '@/components/Chat'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import VueLocalStorage from 'vue-localstorage'
import VueUpload from 'vue-upload-component'
import VueRouter from 'vue-router'

/*
inject dependencies
*/

Vue.use(ElementUI)
Vue.use(VueLocalStorage)
Vue.use(VueResource)
Vue.use(VueRouter)
Vue.component('file-upload', VueUpload)

/*
test
*/

describe('Chat.vue', () => {

    it('should resume chat session if conversation id exists', () => {
    	Vue.localStorage.set('zeusId', 1)
        const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
        promiseCall.resolves({
            body: {
                messages: ['mock_message1'],
                fact_entities: ['mock_fact1'],
                name: 'Bruce'
            }
        })
    	const spy = sinon.spy(Chat.methods, 'getChatHistory')
        const vm = new Vue(Chat).$mount()
        expect(spy.called).to.be.true
        Chat.methods.getChatHistory.restore()
        Vue.localStorage.remove('zeusId')
        Vue.http.get.restore()
    })

    it('should init new chat session if conversation id doesn\'t exist', () => {
    	const spy = sinon.spy(Chat.methods, 'getChatHistory')
        const vm = new Vue(Chat).$mount()
        expect(spy.called).to.be.false
        Chat.methods.getChatHistory.restore()
    })

    it('should successfully init new session', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.resolves({
    		body: {
    			conversation_id: 1
    		}
    	})
    	const spy = sinon.spy(Chat.methods, 'sendUserMessage')
    	const vm = new Vue(Chat).$mount()
    	vm.initChatSession()
    	expect(Vue.localStorage.get('zeusId')).to.be.equal('1')
    	expect(vm.user.input).to.be.equal('')
        expect(spy.called).to.be.true
        expect(vm.uploadUrl).to.be.equal(vm.api_url + 'conversation/1/files')
        expect(vm.connectionError).to.be.false
        Chat.methods.sendUserMessage.restore()
        Vue.http.post.restore()
        Vue.localStorage.remove('zeusId')
    })

    it('should fail to init new session', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.rejects()
    	const vm = new Vue(Chat).$mount()
    	vm.initChatSession()
        expect(vm.connectionError).to.be.true
        Vue.http.post.restore()
    })

    it('should successfully send user feedback', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.resolves({})
    	const vm = new Vue(Chat).$mount()
    	vm.sendFeedback(true)
        expect(vm.promptFeedback).to.be.false
        Vue.http.post.restore()
    })

    it('should handle the failure of sending user feedback ', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	const vm = new Vue(Chat).$mount()
    	vm.sendFeedback()
        promiseCall.rejects()
        expect(vm.connectionError).to.be.true
        Vue.http.post.restore()
    })

    it('should successfully send message and config chat (1)', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.resolves({
    		body: {
    			message: 'mock',
    			file_request: ['yes'],
    			possible_answers: '["yes"]',
    			enforce_possible_answer: true
    		}
    	})
    	const clock = sinon.useFakeTimers();
    	const spy = sinon.spy(Chat.methods, 'configChat')
    	const vm = new Vue(Chat).$mount()
    	vm.sendUserMessage()
    	clock.tick(1500);
    	expect(spy.called).to.be.true
    	Chat.methods.configChat.restore()
    	Vue.http.post.restore()
    	clock.restore();
    })

    it('should successfully send message and config chat (2)', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.resolves({
    		body: {
    			html: 'mock',
    			file_request: ['yes'],
    			enforce_possible_answer: true
    		}
    	})
    	const clock = sinon.useFakeTimers();
    	const spy = sinon.spy(Chat.methods, 'configChat')
    	const vm = new Vue(Chat).$mount()
    	vm.sendUserMessage()
    	clock.tick(1500);
    	expect(spy.called).to.be.true
    	Chat.methods.configChat.restore()
    	Vue.http.post.restore()
    	clock.restore();
    })

    it('should successfully send message and config chat (3)', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.resolves({
    		body: {
    			text: 'mock',
    			file_request: ['yes'],
    			enforce_possible_answer: true,
    			possible_answers: 'null'
    		}
    	})
    	const clock = sinon.useFakeTimers();
    	const spy = sinon.spy(Chat.methods, 'configChat')
    	const vm = new Vue(Chat).$mount()
    	vm.sendUserMessage()
    	clock.tick(1500);
    	expect(spy.called).to.be.true
    	Chat.methods.configChat.restore()
    	Vue.http.post.restore()
    	clock.restore();
    })

    it('should fail to send message', () => {
    	const promiseCall = sinon.stub(Vue.http, 'post').returnsPromise()
    	promiseCall.rejects()
    	const vm = new Vue(Chat).$mount()
    	vm.sendUserMessage()
    	expect(vm.connectionError).to.be.true
    	Vue.http.post.restore()
    })

    it('should get chat history', () => {
        Vue.localStorage.set('zeusId', 1)
        const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
        promiseCall.resolves({
            body: {
                messages: ['mock_message1'],
                fact_entities: ['mock_fact1'],
                name: 'Bruce'
            }
        })
        const spy = sinon.spy(Chat.methods, 'configChat')
        const vm = new Vue(Chat).$mount()
        vm.zeus.input = true
        vm.getChatHistory()
        expect(spy.called).to.be.true
        Chat.methods.configChat.restore()
        Vue.localStorage.remove('zeusId')
        Vue.http.get.restore()
    })

    it('should fail to get chat history', () => {
    	const promiseCall = sinon.stub(Vue.http, 'get').returnsPromise()
    	promiseCall.rejects()
    	const vm = new Vue(Chat).$mount()
    	vm.getChatHistory()
    	expect(vm.connectionError).to.be.true
    	Vue.http.get.restore()
    })

    it('should logout', () => {
        const Component = Vue.extend(Chat)
        const vm = new Component({
            router: new VueRouter({
                routes: [
                    {
                        path: '/'
                    }
                ]
            })
        }).$mount()
        vm.isLoggedIn = true
    })

})
